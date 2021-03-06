# -*- encoding: utf-8 -*-

from up.settings import DUMP_DIR
from popen_call import my_call, message
from download_upload import download_file, upload_file

idp_xml = '''
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
from sys import argv

name = argv[1]
tree = ET.parse('saml-config.xml')
root = tree.getroot()

tag = root.tag.replace('}config', '}')
idp = root.find(tag + 'idp')
keys = idp.find(tag + 'key-store')
auth = idp.find(tag + 'authorization')
clients = auth.find(tag + 'clients')

furl = keys.attrib['url']
issu = idp.attrib['issuer']
pswd = keys.attrib['password']
cont = keys.attrib['container']
new_issuer = issu.split('/')
new_issuer = '{}/{}'.format(new_issuer[0], name)
with open('idpconfig.sh', 'w+') as F:
	config = 'pswd={P}\\ncont={C}\\nissu={I}'.format(P=pswd, C=cont, I=issu)
	F.write(config)

def add_new_client():
	new_clnt = ET.SubElement(clients, tag + 'client', attrib={'issuer': new_issuer})
	new_clnt_tk = ET.SubElement(new_clnt, tag + 'trusted-key')
	ET.SubElement(new_clnt_tk, tag + 'key-store', attrib={
		'container': cont,
		'password': pswd,
		'type': 'JKS',
		'url': furl})
	xml = ET.tostring(root).split()
	xml = ' '.join(xml).replace('> <', '><')
	xml = parseString(xml)
	xml = xml.toprettyxml(indent='    ')
	with open('saml-config.xml', 'w') as xml_file:
		xml_file.write(xml)


client_exists = False
for client in clients:
	if client.get('issuer', new_issuer) == new_issuer:
		client_exists = True

if not client_exists:
	add_new_client()
	print 'restart'
'''

client_xml = '''
<config xmlns="http://krista.ru/idp-config">
    <idp-client issuer="${issu%%/*}/$name" assertionService="$appurl/login">
        <id-providers>
            <provider logout-url="$nsiurl/idp?logout=1"
                      service="$nsiurl/idp/saml"
                      title="Единый вход"
                      issuer="$issu"
                      name="${issu%%/*}.idp"
                      protocol="saml/v2"
                      deflated="false"
                      binding="post">
                <key-store type="JKS" container="$cont" password="$pswd" url="file://$fold/config/keys/keys.jks"/>
                <trusted-keys><x509certificate url="file://$fold/config/keys/idp.crt"/></trusted-keys>
                <roles>idp</roles>
            </provider>
        </id-providers>
        <authentication propagate-roles="true"/>
    </idp-client>
</config>
'''

client_auth = '''
saml=true
idp.default-idp=${issu%%/*}.idp
saml.config-uri=file://$fold/config/saml-config.xml
sso.join.usermanager-class=ru.krista.retools.login.RetoolsUserManager
'''


def description(args, log):
	log.write("\nAdd this server %s as client to IDP" % args.server)


def run(args, log):

	error = 0
	idp_addr = args.dump[0]
	idp_path = args.dump[1]
	name = args.dump[2]
	arch = 'idp_{uniq}.zip'.format(uniq=args.key)

	# -------------------{ Connect to IDP server add client and download config }------------------
	command = [
		'ssh', idp_addr,
		''' cd {idp}/config
			data=$(python -c "{parser}" {name} || ((error+=$?)))
			cd {idp}
			
			case $data in 'restart')
				printf "\n<b>Добавляю клиента {name} на сервер {srv} и перезапускаю IDP</b>\n"
				./krupd jboss.stop  || ((error+=$?))
				./krupd jboss.start || ((error+=$?));;
			esac
			
			zip -jryq {idp}/temp/{arch} {idp}/config/*
			exit $error
		'''.format(
			parser=idp_xml,
			srv=idp_addr,
			idp=idp_path,
			arch=arch,
			name=name,
		)
	]

	error += my_call(command, log)
	download = {'file': ['{idp}/temp/{arch}'.format(idp=idp_path, arch=arch)], 'dest': DUMP_DIR, 'kill': True}
	error += download_file(download, idp_addr, log, silent=True)

	# -------------------{ Copy config to target server }------------------------------------------
	message('\n<b>Копирую конфиги с сервера {S}</b>\n'.format(S=idp_addr), log)
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	upload = {'file': ['{dir}/{arch}'.format(dir=DUMP_DIR, arch=arch)], 'dest': tmp_dir}
	error += upload_file(upload, args.server, log, kill=True)

	# -------------------{ Connect to target server and apply IDP config }-------------------------
	command = [
		'ssh', args.server,
		''' mkdir -p  {wdir}/config
			cd        {wdir}/config
			unzip -oq {wdir}/temp/{key}/{arch}
			name={name}
			fold={wdir}
			conf={wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml			
			prot=( $(grep krista.webadmin.protocol.name $conf) ); prot=${{prot[2]//'value="'/}}; prot=${{prot//'"/>'/}}
			addr=( $(grep krista.webadmin.mail.apphost  $conf) ); addr=${{addr[2]//'value="'/}}; addr=${{addr//'"/>'/}}
			appurl=$prot$addr
			nsiurl=$(grep 'nsi.server.url' auth-profile.properties); nsiurl=${{nsiurl##*=}}
			. ./idpconfig.sh; rm idpconfig.sh # get vars: $issu, $cont, $pswd and remove this file			
			
			cat > saml-config.xml << EOF{client}EOF
			cat > auth-profile.properties << EOF{auth}EOF
			
			chmod 600 *
			mkdir keys
			chmod 700 keys						
			mv *.crt *.jks keys
			
			# add system property
			pname="ru.krista.login.auth-profile"
			value="file://{wdir}/config/auth-profile.properties"
			{wdir}/jboss-bas-*/bin/jboss-cli.sh -c commands="/system-property=$pname:add(value='$value')"
			
			# redeploy login.war
			touch {wdir}/jboss-bas-*/standalone/deployments/login.war
			
			exit $error
		'''.format(
			client=client_xml,
			auth=client_auth,
			parser=idp_xml,
			wdir=args.wdir,
			key=args.key,
			idp=idp_path,
			arch=arch,
			name=name,
		)
	]

	error += my_call(command, log)
	remove_tmp = ['ssh', args.server, 'rm -rf {tmp}'.format(tmp=tmp_dir)]
	my_call(remove_tmp, log)
	return error

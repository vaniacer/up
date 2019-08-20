# -*- encoding: utf-8 -*-

from download_upload import upload_file, download_file
from popen_call import my_call, message
from xml_parser import xml_parser
from up.settings import DUMP_DIR
from os.path import basename


def description(args, log):
	scripts = '\n'.join(basename(script) for script in args.script)
	log.write('\nRun SQL script(s):\n{scripts}\non server {server}\n'.format(scripts=scripts, server=args.server))


def run(args, log):

	error = 0
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	cnf_dir = '{wdir}/jboss-bas-*/standalone/configuration'.format(wdir=args.wdir)

	scripts = [script for script in args.script if '.sql' in script]  # create .sql list
	if not scripts:
		message('\n<b>В списке нет SQL скриптов.</b>\n', log)
		return 1

	message('\n<b>Копирую файл(ы):</b>\n', log)
	upload = {'file': scripts, 'dest': tmp_dir}
	error += upload_file(upload, args.server, log)

	scripts = ['{tmp}/{scr}'.format(tmp=tmp_dir, scr=basename(script)) for script in scripts]

	# ------------------{ Run SQL script }---------------------------------
	command = [
		'ssh', args.server,
		''' cd {conf}
			data=($(python -c "{parser}"))
			dbhost=${{data[0]}}
			dbport=${{data[1]}}
			dbname=${{data[2]}}
			dbuser=${{data[3]}}
			dbpass=${{data[4]}}
			cd - &> /dev/null
			
			export PGPASSWORD="$dbpass"
			dbopts="-h $dbhost -p $dbport -U $dbuser -d $dbname"
			
			for script in {scripts}; {{
			
				filename=$(basename $script)
				log_path="${{script}}_{srv}.log"
				
				printf "\n<b>Выполняю скрипт $filename, тело скрипта:</b>\n<i>"
				cat "$script" | sed 's|<|\&lt\;|g;s|>|\&gt\;|g'

				psql -v ON_ERROR_STOP=1 $dbopts < "$script" &> $log_path || ((error+=$?))
				
				printf "</i>\n\n<b>Результат:</b>\n"
				cat "$log_path" | sed 's|<|\&lt\;|g;s|>|\&gt\;|g'
			}}
			exit $error
		'''.format(
			scripts=' '.join(scripts),
			parser=xml_parser,
			srv=args.server,
			conf=cnf_dir,
			tmp=tmp_dir,
		)
	]

	error += my_call(command, log)

	# ------------------{ Download logs }---------------------------------
	download_list = ['{scr}_{srv}.log'.format(srv=args.server, scr=script) for script in scripts]
	download = {'file': download_list, 'dest': DUMP_DIR, 'kill': False}
	error += download_file(download, args.server, log, link=True, silent=True)

	# ------------------{ Delete tmp folder }-----------------------------
	remove_tmp = ['ssh', args.server, 'rm -rf {tmp}'.format(tmp=tmp_dir)]
	my_call(remove_tmp, log)
	return error

# -*- encoding: utf-8 -*-

from subprocess import check_output
import xml.etree.cElementTree as ET


def parser(xml):
	root = ET.fromstring(xml)
	tag = root.tag.replace('}server', '}')
	pro = root.find(tag + 'profile')
	for child in pro:
		if 'datasources' in child.tag:
			data_tag = child.tag.replace('}subsystem', '}')
			sub_data = child
			break

	for child in sub_data[0]:
		if child.attrib:
			if child.attrib['pool-name'] == 'DataaccessDS':
				connection = child.find(data_tag + 'connection-url').text
				security = child.find(data_tag + 'security')
				dbuser = security.find(data_tag + 'user-name').text
				dbpass = security.find(data_tag + 'password').text
				break

	splitted_connection = connection.split('/')
	dbport = splitted_connection[-2].split(':')[-1]
	dbhost = splitted_connection[-2].split(':')[0]
	dbname = splitted_connection[-1]

	return dbhost, dbport, dbname, dbuser, dbpass


def get_db_parameters(server, filename):
	command = ['ssh', server, 'cat %s' % filename]
	try:
		xml = check_output(command)
		return parser(xml)
	except:
		return '', '', '', '', ''

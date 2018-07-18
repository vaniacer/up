# -*- encoding: utf-8 -*-

import xml.etree.cElementTree as ET
from subprocess import check_output


def parser(xml):
	tree = ET.fromstring(xml)
	iter_ = tree.getiterator()
	connection = ''
	username = ''
	password = ''

	for elem in iter_:
		name = elem.get('pool-name')
		if name == 'DataaccessDS':
			prefix = elem.tag.replace('}datasource', '}')
			children = elem.getchildren()
			for child in children:
				if child.tag == '{}connection-url'.format(prefix):
					connection = child.text
				if child.tag == '{}security'.format(prefix):
					sec_children = child.getchildren()
					for sec_child in sec_children:
						if sec_child.tag == '{}user-name'.format(prefix):
							username = sec_child.text
						if sec_child.tag == '{}password'.format(prefix):
							password = sec_child.text

	splitted_connection = connection.split('/')
	dbport = splitted_connection[-2].split(':')[-1]
	dbhost = splitted_connection[-2].split(':')[0]
	dbname = splitted_connection[-1]
	dbuser = username
	dbpass = password

	return dbhost, dbport, dbname, dbuser, dbpass


def get_db_parameters(server, filename):
	get_xml = ['ssh', server, 'cat %s' % filename]
	xml = check_output(get_xml)
	return parser(xml)

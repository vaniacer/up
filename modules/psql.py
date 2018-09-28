# -*- encoding: utf-8 -*-

from modules.uniq import uniq
from datetime import datetime
from subprocess import call, check_output
from conf import dbname, dbhost, dbpass, dbport, dbuser


def psql(query, select=False):
	"""Клиент посгреса."""

	psql_opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-tAc', query]
	if select:
		data = check_output(psql_opt, env={"PGPASSWORD": dbpass})
		return data
	else:
		error = call(psql_opt, env={"PGPASSWORD": dbpass})
		return error


def cron_log(args, error, log):
	"""Создает лог после выполнения задания в кроне."""

	today = datetime.today()
	date = today.strftime('%Y-%m-%d %H:%M')
	data = psql("SELECT perm, name, proj_id, user_id, serv_id FROM ups_job WHERE cron='{}';".format(args.key), True)
	perm, name, proj_id, user_id, serv_id = data.split('|')

	sql = u'''
		INSERT INTO ups_history VALUES
		(DEFAULT, current_timestamp, '{name}', '{cron}', '{cdat}', {exit}, '', {proj}, {user}, '{uniq}', {serv});
		UPDATE ups_history SET \"desc\" = $$ {desc} $$ WHERE uniq='{uniq}';
	'''.format(
		cron=args.key,
		proj=proj_id,
		serv=serv_id,
		user=user_id,
		uniq=uniq(),
		exit=error,
		name=name,
		cdat=date,
		desc=log,)

	if perm == 'f':
		sql += u"DELETE FROM ups_job WHERE cron='{}';".format(args.key)

	psql(sql)


def regular_log(args, error, log):
	"""Логирует все остальные комманды."""

	sql = u"UPDATE ups_history SET \"desc\" = $$ {desc} $$, exit={exit} WHERE uniq='{uniq}';".format(
		uniq=args.key,
		exit=error,
		desc=log,)

	if args.cron:
		sql += u"UPDATE ups_job SET \"desc\" = $$ {desc} $$ WHERE cron='{cron}';".format(
			cron=args.key,
			desc=log,)

	psql(sql)

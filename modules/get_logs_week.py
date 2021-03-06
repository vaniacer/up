# -*- encoding: utf-8 -*-

from datetime import datetime
from modules.uniq import uniq
from popen_call import my_call, message
from download_upload import download_file


def description(args, log):
	log.write('\nGet week logs from server:\n%s' % args.server)


def run(args, log):

	filename = '{server}_weeklogs_{date:%d-%m-%Y}.zip'.format(server=args.server, date=datetime.now())
	message('\n<b>Копирую файл - {file}</b>\n'.format(file=filename), log)

	download = {'file': ['{wdir}/temp/{file}'.format(wdir=args.wdir, file=filename)], 'dest': ''}
	command = [
		'ssh', args.server,
		''' find {wdir}/jboss-bas-*/standalone/log -type f -daystart -ctime -6 | xargs zip -jy {file} > /dev/null
			for i in ${{PIPESTATUS[@]}}; {{ ((error+=$i)); }}; exit $error
		'''.format(wdir=args.wdir, file=download['file'][0])
	]

	error = my_call(command, log)
	if error == 0:
		error += download_file(download, args.server, log, link=True, limit=args.limit, kill=True)
		message(
			""" \n<b>Команда для быстрого извлечения логов(Linux):</b>
				<div class="input-group col-md-10">
					<div class="input-group-btn">
						<input class="form-control" type="text"
						value="curl {OP} https://ups.krista.ru/dumps/{FN} && unzip -o {FN}" id="{ID}">
						<input onclick="copy_to_clipboard('{ID}')" type="button" value="Copy" class="btn btn-primary"
						title="Copy to clipboard"/>
					</div>
				</div>
			""".format(
				OP='-O --noproxy ups.krista.ru --netrc-file ~/.ups_download',
				PI=args.pid,
				FN=filename,
				ID=uniq(),
			), log
		)
	return error

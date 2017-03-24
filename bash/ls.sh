#!/bin/bash

servers=$@

# Get logs
for server in ${servers[@]}; do

    # server comes like this jboss@localhost:/var/lib/jboss
    # cut address jboss@localhost
    addr=${server%%:*}
    # cut working directory /var/lib/jboss
    wdir=${server##*:}

    echo -e "Сервер - ${addr}\n"
    echo -e "Пакеты обновлений:\n"
    ssh ${addr} "ls ${wdir}/updates/new" || error=$?
    echo

done

exit ${error}
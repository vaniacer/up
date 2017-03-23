#!/bin/bash

error=$?

servers=($@)

# Get logs
for server in "${servers[@]}"; do

    # server comes like this jboss@localhost:/var/lib/jboss
    # cut address jboss@localhost
    addr=${server%%:*}
    # cut working directory /var/lib/jboss
    wdir=${server##*:}

    echo -e "Сервер - ${addr}"
    ssh ${addr} "cat ${wdir}/jboss-bas-*/standalone/log/server.log" || { error+="$? "; break; }
    echo

done

exit ${error}
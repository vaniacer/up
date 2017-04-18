#!/bin/bash

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) servers=${2};;
	    -update | -u) updates=${2};;
        -job    | -j) jobs=${2};;
    esac

    shift 2
done

# Get logs
for server in ${servers[@]}; do

    # server comes like this jboss@localhost:/var/lib/jboss
    # cut address jboss@localhost
    addr=${server%%:*}
    # cut working directory /var/lib/jboss
    wdir=${server##*:}

    name="| Сервер - ${addr} |"
    line=$[ (100-${#name})/2 ]

    printf %.s- $(seq ${line}); printf "${name}"; printf %.s- $(seq ${line})
    echo -e "\nПакеты обновлений:\n"
    ssh ${addr} "ls ${wdir}/updates/new" || error=$?
    echo

done

exit ${error}
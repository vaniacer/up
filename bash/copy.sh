#!/bin/bash

#set -e

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) servers=${2};;
	    -update | -u) updates=${2};;
	           -cron) cron=${2};;
    esac

    shift 2
done

function info () {
    name="| Сервер - ${1} |"
    line=$[ (100-${#name})/2 ]

    printf %.s- $(seq ${line}); printf "${name}"; printf %.s- $(seq ${line}); printf "\n"
}

# Simple copy
for server in ${servers}; do

    # server comes like this jboss@localhost:/var/lib/jboss
    # get address jboss@localhost
    addr=${server%%:*}
    # get working directory /var/lib/jboss
    wdir=${server##*:}

    info ${addr}

    ssh ${addr} "echo > /dev/null" && {

        for file in ${updates}; do
            filename=$(basename ${file})
            echo -e "\nКопирую файл - ${filename}"
            # Check if file exist
            ssh ${addr} ls ${wdir}/updates/new/${filename} &> /dev/null && {
                echo -e "Файл - ${filename} существует, пропускаю."; }  || {
                # Copy if not exist
                scp ${file} ${server}/updates/new || error="$?"; }
            echo
        done
    } || { error=$?; echo -e "\nServer unreachable."; }

    echo
done

[ "${cron}" ] && echo "Error code: ${error}"
exit ${error}
#!/bin/bash

#set -e

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) server=true; update=false; shift;;
	    -update | -u) update=true; server=false; shift;;
    esac

    [ ${server} = true ] && servers+=($1)
    [ ${update} = true ] && updates+=($1)

    shift
done

# Simple copy
for server in "${servers[@]}"; do

    # server comes like this jboss@localhost:/var/lib/jboss
    # cut address jboss@localhost
    addr=${server%%:*}
    # cut working directory /var/lib/jboss
    wdir=${server##*:}

    echo -e "Сервер - ${addr}"
    ssh ${addr} "echo > /dev/null" && {

        for file in "${updates[@]}"; do
            filename=$(basename ${file})
            echo -e "Копирую файл - ${filename}"
            # Check if file exist
            ssh ${addr} "ls ${wdir}/updates/new/${filename} &> /dev/null" && {
                echo -e "Файл - ${filename} существует, пропускаю."; }    || {
                # Copy if not exist
                scp ${file} ${server}/updates/new; }
            echo
        done
    } || { error="$?"; echo -e "Server unreachable."; }

    echo
done

exit ${error}
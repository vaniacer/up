#!/bin/bash

error=0
folder=$(dirname $0)
crondir=${folder}/../../logs/cron
rundir=${folder}/../../logs/run

#Get opts
until [ -z "$1" ]; do case $1 in

    -server | -s) servers=${2};;
    -update | -u) updates=${2};;
    -job    | -j) jobs=${2};;
           -cron) cron=${2};;
           -desc) desc=${2};;
            -key) key=${2};;

esac; shift 2; done

. ${folder}/func.sh

case ${desc} in true)
    echo -e "Stop dummy page on server(s):\n${servers// /\\n}\n"
    exit 0;;
esac

function run () {
    for server in ${servers}; do
        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost
        addr=${server%%:*}

        # get working directory /var/lib/jboss
        wdir=${server##*:}

        info ${addr}

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} '~/.utils/dp.sh --stop && echo Stop dummy page.' || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

        echo # Add empty line
    done

    echo -e "\nDone.\nERROR: ${error}"
}

starter # From func.sh
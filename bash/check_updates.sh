#!/bin/bash

error=0
folder=$(dirname $0)
crondir=${folder}/../../logs/cron
rundir=${folder}/../../logs/run

echo '' > ${rundir}/err

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) servers=${2};;
	    -update | -u) updates=${2};;
        -job    | -j) jobs=${2};;
    esac

    shift 2
done

function info () {
    name="| Server - ${1} |"
    line=$[ (100-${#name})/2 ]

    printf %.s- $(seq ${line}); printf "${name}"; printf %.s- $(seq ${line}); printf "\n"
}

function run () {
    # Get logs
    for server in ${servers[@]}; do

        # server comes like this jboss@localhost:/var/lib/jboss
        # cut address jboss@localhost
        addr=${server%%:*}
        # cut working directory /var/lib/jboss
        wdir=${server##*:}

        info ${addr}

        echo -e "\nПакеты обновлений:\n"
        ssh ${addr} "ls ${wdir}/updates/new" || error=$?
        echo

    done

    echo -e "\nDone.\nERROR: ${error}"
    echo ${error} > ${rundir}/err
}

run &> ${rundir}/log
exit ${error}
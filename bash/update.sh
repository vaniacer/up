#!/bin/bash

error=0
folder=$(dirname $0)
logdir=${folder}/../../logs/cron

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

function update () {
    echo -e "Not ready yet"
    error=$?
    echo "__ERROR__${error}"
}

log=$(update)
err=$(echo ${log//*__ERROR__})
log=${log//__ERROR__*}
dat=$(date +'%b %d, %Y %R'); dat=${dat//.}; dat=${dat^};

[ "${cron}" ] && { log=${log}"\nDate: ${dat}\nError: ${err}"; echo -e "${log}" > ${logdir}/${cron}; } \
              || { echo -e "${log}"; }

exit ${err}
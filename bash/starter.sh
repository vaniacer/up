#!/bin/bash

error=0
workdir=$(dirname $0)
crondir=${workdir}/../../logs/cron
rundir=${workdir}/../../logs/run
#----------|Get opts|------------
until [ -z "$1" ]; do case $1 in

    -server | -s) servers=${2};;
    -update | -u) updates=${2};;
    -date   | -d) date=${2};;
    -cron   | -C) cron=${2};;
    -desc   | -D) desc=${2};;
    -job    | -j) jobs=${2};;
    -cmd    | -c) cmd=${2};;
    -key    | -k) key=${2};;
    -id     | -i) id=${2};;

esac; shift 2; done
#--------------------------------

function info () {
    name="| Server - ${1} |"; line=$[ (100-${#name})/2 ]
    name=$(printf %.s- $(seq ${line}); printf "${name}"; printf %.s- $(seq ${line}); printf "\n")
    [ ${#name} -lt 100 ] && name=-${name}; echo -e ${name}
}

. ${workdir}/${cmd}

function starter () {
    [ "${desc}" ] && description
    [ "${cron}" ] \
        && { log=$(run);  dat=$(date +'%b %d, %Y %R'); dat=${dat//.}; dat=${dat^}
             log=${log}"\nDate: ${dat}"; echo -e "${log}" > ${crondir}/${cron}; } \
        || { echo       '' > ${rundir}/err${key}
             run          &> ${rundir}/log${key}
             echo ${error} > ${rundir}/err${key}; }

    exit ${error}
}

[ "${desc}" ] && description || starter
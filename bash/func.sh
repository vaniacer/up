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
    -cmd    | -c) cmd=${2};;
    -job    | -j) jobs=${2};;
           -cron) cron=${2};;
           -desc) desc=${2};;
            -key) key=${2};;
             -id) id=${2};;

esac; shift 2; done
#--------------------------------

function info () {
    name="| Server - ${1} |"; line=$[ (100-${#name})/2 ]
    name=$(printf %.s- $(seq ${line}); printf "${name}"; printf %.s- $(seq ${line}); printf "\n")
    [ ${#name} -lt 100 ] && name=-${name}; echo -e ${name}
}

function starter () {
    [ "${cron}" ] \
    && { log=$(run)
         err=$(echo ${log//*ERROR:})
         log=${log//ERROR:*}
         dat=$(date +'%b %d, %Y %R'); dat=${dat//.}; dat=${dat^}
         log=${log}"\nDate: ${dat}\nError: ${err}"; echo -e "${log}" > ${crondir}/${cron}; } \
    || { echo       '' > ${rundir}/err${key}
         run          &> ${rundir}/log${key}
         echo ${error} > ${rundir}/err${key}; }

    exit ${error}
}
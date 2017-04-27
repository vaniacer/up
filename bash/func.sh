#!/bin/bash

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
    || { echo '' > ${rundir}/err${key}
         run    &> ${rundir}/log${key}
         echo ${error} > ${rundir}/err${key}; }

    exit ${error}
}
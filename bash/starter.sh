#!/bin/bash

error=0
workdir=$(dirname $0)
cronfile=/var/spool/cron/crontabs/${USER}
dumpdir=${workdir}/../media/updates/dumps
crondir=${workdir}/../../logs/cron
rundir=${workdir}/../../logs/run
#---------| Get opts |-----------
until [ -z "$1" ]; do case $1 in

    -server | -s) servers=${2};;
    -update | -u) updates=${2};;
    -date   | -d) date=${2};;
    -cron   | -C) cron=${2};;
    -desc   | -D) desc=${2};;
    -job    | -j) jobs=${2};;
    -cmd    | -c) cmd=${2};;
    -run    | -r) run=${2};;
    -key    | -k) key=${2};;
    -id     | -i) id=${2};;

esac; shift 2; done
#--------------------------------

function info () { # Print delimiter line with server name(${1}) in center.
    L=120; B='='; S='<'; E='>'; N="| ${1} |"; l=$[ (${L}-${#N}-${#S}-${#E})/2 ]; line=$(printf %.s${B} $(seq ${l}))
    C=$[ ${#S}+${#N}+${#E}+${#line}*2 ]; [ ${C} -lt ${L} ] && N=${B}${N}; echo -e "${S}${line}${N}${line}${E}\n"
}

function addr () { # Server comes like this - jboss@localhost:/var/lib/jboss.
    #  Get ssh address jboss@localhost and working directory /var/lib/jboss.
    addr=${server%%:*}; wdir=${server##*:}; info "Server - ${addr}"
}

function starter () { [ "${cron}" ] \
    && { run &> ${crondir}/${cron}; dat=$(date +'%b %d, %Y %R'); dat=${dat//.}; dat=${dat^}
         echo -e "\nError: ${error}\nDate: ${dat}" >> ${crondir}/${cron}; } \
    || { run          &> ${rundir}/log${key}
         echo ${error} > ${rundir}/err${key}; }
    exit ${error}
}

. ${workdir}/${cmd} # Load 'run' and 'description' functions from ${cmd}.

[ "${desc}" ] && description || starter
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

function info () { # Print delimiter line with info(${1}) in center.
    [ ${2} ] && { [ ${2} = 0 ] && smile=":) " || smile=":( "; } # Add smile to info if ${2}(error code) is set.
    #Length|Body symbol|Start symbol|End symbol|Center part with info|Calculate number of body symbols |
    L=120  ; B='='     ; S="<"      ; E=">"    ; N="| ${1} ${smile}|"; l=$[ (${L}-${#N}-${#S}-${#E})/2 ]
    line=$(printf %.s${B} $(seq ${l})); C=$[ ${#S}+${#N}+${#E}+${#line}*2 ] # Make line and calculate current length.
    [ ${C} -lt ${L} ] && N=${N}${B};        # Add ${B} if current length less then ${L}.
    printf "\n${S}${line}${N}${line}${E}\n" # Print result.
}

function addr () { # Server comes like this - jboss@localhost:/var/lib/jboss.
    # Cut ssh address 'jboss@localhost' and working directory '/var/lib/jboss'.
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
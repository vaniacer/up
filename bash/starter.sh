#!/bin/bash

error=0
workdir=$(dirname $0)
cronfile=/var/spool/cron/crontabs/${USER}
dumpdir=${workdir}/../media/updates/dumps
crondir=${workdir}/../../logs/cron
rundir=${workdir}/../../logs/run
#---------| Get opts |------------
until [ -z ${1} ]; do case ${1} in

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
#---------------------------------

function info () { # Print delimiter line with info(${1}) in center.
    [ ${2} ] && { [ ${2} = 0 ] && F=':) ' || F=':( '; } # Add a smile to info if ${2}(error code) is set.
    #--------+-------------+--------------+------------+-----------------------+--------------------------------------+
    # Length | Body symbol | Start symbol | End symbol | Center part with info | Calculate number of body symbols     |
    #--------+-------------+--------------+------------+-----------------------+--------------------------------------+
    L=120    ; B='='       ; S='<'        ; E='>'      ; C="| ${1} ${F}|"      ; b=$[(${L}-${#C}-${#S}-${#E})/2]
    #-------------------------------+--------------------------------+------------------------------------------------+
    # Make line segment.            | Calculate current length.      | Add one ${B} if current length less then ${L}. |
    #-------------------------------+--------------------------------+------------------------------------------------+
    N=$(printf %.s${B} $(seq ${b})) ; l=$[${#S}+${#C}+${#E}+${#N}*2] ; [ ${l} -lt ${L} ] && C=${C}${B}
    printf "\n${S}${N}${C}${N}${E}\n" # Print result.
}

function addr () {
    # Server comes like this - jboss@localhost:/var/lib/jboss, split it to:
    #-----------------+-------------------+-------------------------------+
    # Ssh address     | Working directory | And show ${addr} as info      |
    #-----------------+-------------------+-------------------------------+
    addr=${server%%:*}; wdir=${server##*:}; info "Server - ${addr}"
}

function download () { # Used in backup_* and get_dump. SCP files to ${dumpdir} and add 'download' button in output.
    [ "${cron}" ] && { name=$(tail -n2 ${crondir}/${cron}) ; } \
                  || { name=$(tail -n2 ${rundir}/log${key}); }
                       name=${name#*\"}; name=${name//\"./}

    echo -e "Копирую файл - ${name}"; scp ${addr}:${name} ${dumpdir} || error=$?
    echo -e "\n<a class='btn btn-primary' href='/updates/dumps/${name//\/*\//}'>Download</a>\n"
}

function starter ()  { # Run command now or set a cronjob.
    [ "${cron}" ] && { run &> ${crondir}/${cron}; dat=$(date +'%b %d, %Y %R'); dat=${dat//.}; dat=${dat^}
                       echo -e "\nError: ${error}\nDate: ${dat}" >> ${crondir}/${cron}; } \
                  || { run          &> ${rundir}/log${key}
                       echo ${error} > ${rundir}/err${key}; }
    exit ${error}
}

. ${workdir}/${cmd} # Load 'run' and 'description' functions from ${cmd}.

[ "${desc}" ] && description || starter
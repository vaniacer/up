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
	           -desc) desc=${2};;
    esac

    shift 2
done

case ${desc} in true)
    echo -e "Copy Updates:\n${updates// /\\n}\nto Servers:\n${servers// /\\n}\n"
    exit 0;;
esac

function info () {
    name="| Сервер - ${1} |"
    line=$[ (100-${#name})/2 ]

    printf %.s- $(seq ${line}); printf "${name}"; printf %.s- $(seq ${line}); printf "\n"
}

function copy () {
    for server in ${servers}; do

        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost
        addr=${server%%:*}

        # get working directory /var/lib/jboss
        wdir=${server##*:}

        info ${addr}

        ssh ${addr} "echo > /dev/null" \
            && { for file in ${updates}; do
                    filename=$(basename ${file})
                    echo -e "\nКопирую файл - ${filename}"

                    # Check if file exist, copy if not exist
                    ssh ${addr} ls ${wdir}/updates/new/${filename} &> /dev/null \
                        && { echo -e "Файл - ${filename} существует, пропускаю."; } \
                        || { scp ${file} ${server}/updates/new || error="$?"; }

                    echo # Add empty line
                done; } \
            || { error=$?; echo -e "\nServer unreachable."; }

        echo # Add empty line
    done

    echo "__ERROR__${error}"
}

log=$(copy)
err=$(echo ${log//*__ERROR__})
log=${log//__ERROR__*}
dat=$(date +'%b %d, %Y %R'); dat=${dat//.}; dat=${dat^};

[ "${cron}" ] && { log=${log}"\nDate: ${dat}\nError: ${err}"; echo -e "${log}" > ${logdir}/${cron}; } \
              || { echo -e "${log}"; }

exit ${err}
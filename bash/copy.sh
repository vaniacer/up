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
    echo -e "Copy Updates:\n${updates// /\\n}\n\nto Servers:\n${servers// /\\n}\n"
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

        ssh ${addr} "echo > /dev/null" \
            && { for file in ${updates}; do
                    filename=$(basename ${file})
                    echo -e "\nCopy file - ${filename}"

                    # Check if file exist, copy if not exist
                    ssh ${addr} ls ${wdir}/updates/new/${filename} &> /dev/null \
                        && { echo -e "File - ${filename} exist, skip."; } \
                        || { scp ${file} ${server}/updates/new || error="$?"; }

                    echo # Add empty line
                done; } \
            || { error=$?; echo -e "\nServer unreachable."; }

        echo # Add empty line
    done

    echo -e "\nDone.\nERROR: ${error}"
}

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
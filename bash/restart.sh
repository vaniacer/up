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
    echo -e "Restart servers:\n${servers// /\\n}\n"
    exit 0;;
esac

function run () {
    echo -e "Not ready yet"
    error=$?
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
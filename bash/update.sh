#!/bin/bash

error=0
folder=$(dirname $0)
crondir=${folder}/../../logs/cron
rundir=${folder}/../../logs/run

echo '' > ${rundir}/err

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) servers=${2};;
	    -update | -u) updates=${2};;
	    -job    | -j) jobs=${2};;
	           -cron) cron=${2};;
               -desc) desc=${2};;
    esac

    shift 2
done

case ${desc} in true)
    echo -e "Update servers:\n${servers// /\\n}\n\nwith updates:\n${updates// /\\n}\n"
    exit 0;;
esac

function info () {
    name="| Сервер - ${1} |"
    line=$[ (100-${#name})/2 ]

    printf %.s- $(seq ${line}); printf "${name}"; printf %.s- $(seq ${line}); printf "\n"
}

function run () {
    echo -e "Not ready yet"
    error=$?
    echo -e "\nDone.\nERROR: ${error}"
    echo ${error} > ${rundir}/err
}

[ "${cron}" ] \
&& { log=$(run)
     err=$(echo ${log//*ERROR:})
     log=${log//ERROR:*}
     dat=$(date +'%b %d, %Y %R'); dat=${dat//.}; dat=${dat^}
     log=${log}"\nDate: ${dat}\nError: ${err}"; echo -e "${log}" > ${crondir}/${cron}; } \
|| { run &> ${rundir}/log; }

exit ${err}
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
            -key) key=${2};;

esac; shift 2; done

echo '' > ${rundir}/err${key}
. ${folder}/func.sh

function run () {
    # Get logs
    for server in ${servers[@]}; do

        # server comes like this jboss@localhost:/var/lib/jboss
        # cut address jboss@localhost
        addr=${server%%:*}
        # cut working directory /var/lib/jboss
        wdir=${server##*:}

        info ${addr}
        ssh  ${addr} "cat ${wdir}/jboss-bas-*/standalone/log/server.log" || error=$?
        echo

    done

    echo -e "\nDone.\nERROR: ${error}"
    echo ${error} > ${rundir}/err${key}
}

run &> ${rundir}/log${key}
exit ${error}
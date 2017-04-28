#!/bin/bash

# Get options and functions
. $(dirname $0)/func.sh

function run () { #----------------------------------|Main function|----------------------------------------------------
    echo '' > ${rundir}/err${key}
    for server in ${servers}; do
        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost and working directory /var/lib/jboss
        addr=${server%%:*}; wdir=${server##*:}; info ${addr} # add delimiter string with server name

        echo -e "\nПакеты обновлений:\n"
        ssh ${addr} "ls ${wdir}/updates/new" || error=$?
        echo

    done

    echo -e "\nDone.\nERROR: ${error}"
    echo ${error} > ${rundir}/err${key}
} #---------------------------------------------------------------------------------------------------------------------

run &> ${rundir}/log${key}
exit ${error}
#!/bin/bash

function run () { #----------------------------------|Main function|----------------------------------------------------
    echo '' > ${rundir}/err${key}
    for server in ${servers}; do
        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost and working directory /var/lib/jboss
        addr=${server%%:*}; wdir=${server##*:}; info ${addr} # add delimiter string with server name

        ssh  ${addr} "cat ${wdir}/jboss-bas-*/standalone/log/server.log" || error=$?
        echo

    done

    echo -e "\nDone.\nERROR: ${error}"
    echo ${error} > ${rundir}/err${key}
} #---------------------------------------------------------------------------------------------------------------------
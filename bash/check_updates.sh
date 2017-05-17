#!/bin/bash

function description () {
    echo -e "Show updates of server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do
        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost and working directory /var/lib/jboss
        addr=${server%%:*}; wdir=${server##*:}; info ${addr} # add delimiter string with server name

        echo -e "\nПакеты обновлений:\n"
        ssh ${addr} "ls ${wdir}/updates/new" || error=$?

        echo # Add empty line
    done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
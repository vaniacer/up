#!/bin/bash

function description () {
    echo -e "Delete all Updates from Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do
        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost and working directory /var/lib/jboss
        addr=${server%%:*}; wdir=${server##*:}; info ${addr} # add delimiter string with server name

        # Check access
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} "echo -e \"Delete files:\n$(ls ${wdir}/updates/new)\""
                 ssh ${addr} "rm ${wdir}/updates/new/*" || error=$?
                 # Add empty line
                 echo; } \
            || { error=$?; echo -e "\nServer unreachable."; }

        echo # Add empty line
    done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
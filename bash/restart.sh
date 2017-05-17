#!/bin/bash

function description () {
    echo -e "Restart server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} ${wdir}/krupd jboss.stop  || error=$?
                 ssh ${addr} ${wdir}/krupd jboss.start || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
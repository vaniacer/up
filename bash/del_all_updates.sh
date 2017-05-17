#!/bin/bash

function description () {
    echo -e "Delete all Updates from Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do addr

        # Check access
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} "echo -e \"Delete files:\n$(ls ${wdir}/updates/new)\""
                 ssh ${addr} "rm ${wdir}/updates/new/*" || error=$?; echo; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
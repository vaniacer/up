#!/bin/bash

function description () {
    echo -e "Delete Update(s):\n${updates// /\\n}\n\nfrom Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do
        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost and working directory /var/lib/jboss
        addr=${server%%:*}; wdir=${server##*:}; info ${addr} # add delimiter string with server name

        # Check access
        ssh ${addr} "echo > /dev/null" \
            && { for file in ${updates}; do
                    filename=$(basename ${file})
                    echo -e "Delete file - ${filename}."
                    ssh ${addr} "rm ${wdir}/updates/new/${filename}" || error=$?

                    echo # Add empty line
                done; } \
            || { error=$?; echo -e "\nServer unreachable."; }

        echo # Add empty line
    done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
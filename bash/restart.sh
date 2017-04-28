#!/bin/bash

# Get options and functions
. $(dirname $0)/func.sh

case ${desc} in true) echo -e "Restart server(s):\n${servers// /\\n}\n"; exit 0;; esac
function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do
        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost and working directory /var/lib/jboss
        addr=${server%%:*}; wdir=${server##*:}; info ${addr} # add delimiter string with server name

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} ${wdir}/krupd jboss.stop  || error=$?
                 ssh ${addr} ${wdir}/krupd jboss.start || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

        echo # Add empty line
    done

    echo -e "\nDone.\nERROR: ${error}"
} #---------------------------------------------------------------------------------------------------------------------

starter # From func.sh
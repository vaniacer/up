#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------ #---------------------| Function description |------------------------------------------------
    echo -e "Backup database on server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; do addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} "${wdir}/krupd bkp db" || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; info 'Done'
} #---------------------------------------------------------------------------------------------------------------------
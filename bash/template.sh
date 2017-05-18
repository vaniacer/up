#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Put description here. Variables: ${servers} ${updates} ${jobs} ${cmd}. Example:
    Copy Update(s):\n${updates// /\\n}\n\nto Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; do addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} echo "Put your code here" || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; info 'Done'
} #---------------------------------------------------------------------------------------------------------------------
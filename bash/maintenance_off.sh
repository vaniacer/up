#!/bin/bash

function description () {
    echo -e "Stop dummy page on server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} '~/.utils/dp.sh --stop && echo Stop dummy page.' || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
#!/bin/bash

function description () {
    echo -e "Copy utils folder to server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} [ -d '.utils' ] || mkdir .utils || error=$?
                 scp -r ~/utils/* ${addr}:~/.utils || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
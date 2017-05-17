#!/bin/bash

function description () {
    echo -e "Copy utils folder to server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do
        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost and working directory /var/lib/jboss
        addr=${server%%:*}; wdir=${server##*:}; info ${addr} # add delimiter string with server name

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} [ -d '.utils' ] || mkdir .utils || error=$?
                 scp -r ~/utils/* ${addr}:~/.utils || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

        echo # Add empty line
    done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
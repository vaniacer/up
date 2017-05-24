#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show system info from server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; do addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} "
                    echo Hostname: \${HOSTNAME}; echo

                    echo Interfaces: \$(ip a | grep 'inet ' | grep -v '127.0.0.1' | sed 's/inet //g; s|/.*$||g'); echo

                    echo Uptime: \$(uptime); echo

                    echo Logged in Users:
                    w; echo

                    echo Memory:
                    free -h; echo

                    echo Disk:
                    df -h; echo; df -ih; echo

                    echo Processes:
                    top -b -n1

                    " || error=$?
            } \
            || { error=$?; echo -e "\nServer unreachable."; }

    done; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
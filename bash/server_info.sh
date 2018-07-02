#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow system info of server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    # Add server name coz this command not stored in history and don't have event.serv.name
    printf "\n-----{ <b>Server $addr</b> }-----\n"

    ssh_yes "$sopt $addr" > /dev/null

    ssh -t -t $sopt $addr "
        printf '\n<b>Hostname:</b>\n'
        hostname

        printf '\n<b>Interfaces:</b>\n'
        ip a | grep 'inet ' | sed '/127.0.0.1/d; s/.*inet //g; s|/.*$||g'

        printf '\n<b>Memory:</b>\n'
        free -h

        printf '\n<b>CPU:</b>\n'
        lscpu

        printf '\n<b>Disk:</b>\n'
        df -h; echo; df -ih; echo; lsblk

        printf '\n<b>Software:</b>\n'
        uname -a; echo
        [ -e /usr/bin/lsb_release ] && { lsb_release -a; echo; }
        [ -e /usr/bin/java        ] && { java  -version; echo; }
        [ -e /usr/bin/psql        ] && { psql  -V      ; echo; }
        [ -e /usr/sbin/nginx      ] && { nginx -v      ; echo; }

        printf '<b>Logged in Users:</b>\n'
        who

        printf '\n<b>Processes:</b>\n'
        top -bn1" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show system info from server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh ${addr} "
        printf '\n<b>Hostname:</b>' \$(hostname)

        printf '\n<b>Interfaces:</b>'
        ip a | grep 'inet ' | sed '/127.0.0.1/d; s/inet //g; s|/.*$||g'

        printf '\n<b>Memory:</b>'
        free -h

        printf '\n<b>CPU:</b>'
        lscpu

        printf '\n<b>Disk:</b>'
        df -h; echo; df -ih; echo; lsblk

        printf '\n<b>Software:</b>'
        uname -a; echo
        [ -e /usr/bin/lsb_release ] && { lsb_release -a; echo; }
        [ -e /usr/bin/java        ] && { java  -version; echo; }
        [ -e /usr/bin/psql        ] && { psql  -V      ; echo; }
        [ -e /usr/sbin/nginx      ] && { nginx -v      ; echo; }

        printf '<b>Logged in Users:</b>'
        who

        printf '\n<b>Processes:</b>'
        top -b -n1" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
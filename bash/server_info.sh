#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nShow system info of server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    expect_ssh "$sopt" "$addr" > /dev/null

    printf "\n"
    ssh $sopt $addr "
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
        top -b -n1" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
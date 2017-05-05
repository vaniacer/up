#!/bin/bash

function description () {
    echo -e "Get DB dump from server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do
        # server comes like this jboss@localhost:/var/lib/jboss
        # get address jboss@localhost and working directory /var/lib/jboss
        addr=${server%%:*}; wdir=${server##*:}; info ${addr} # add delimiter string with server name

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} "${wdir}/krupd bkp db" || error=$?
                 name=$(tail -n2 ${rundir}/log${key}); name=${name#*\"}; name=${name//\"./}
                 echo -e "Копирую файл - ${name}"; scp ${addr}:${name} ${dumpdir} || error=$?
                 echo -e " Удаляю файл - ${name}"; ssh ${addr} "rm ${name}"       || error=$?;
                 echo -e "\n<a href='/updates/dumps/${name//\/*\//}'>download</a>"; } \
            || { error=$?; echo -e "\nServer unreachable."; }

        echo # Add empty line
    done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
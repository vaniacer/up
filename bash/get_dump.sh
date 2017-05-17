#!/bin/bash

function description () {
    echo -e "Get DB dump from server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for server in ${servers}; do addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} "${wdir}/krupd bkp db" || error=$?
                 [ "${cron}" ] \
                    && { name=$(tail -n2 ${crondir}/${cron});  } \
                    || { name=$(tail -n2 ${rundir}/log${key}); }
                 name=${name#*\"}; name=${name//\"./}

                 echo -e "Копирую файл - ${name}"; scp ${addr}:${name} ${dumpdir} || error=$?
                 echo -e " Удаляю файл - ${name}"; ssh ${addr} "rm ${name}"       || error=$?;
                 echo -e "\n<a href='/updates/dumps/${name//\/*\//}'>download</a>"; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Backup full on server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { [ ${1} ] || addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh ${addr} "${wdir}/krupd bkp db"  || error=$?; download
                 ssh ${addr} "${wdir}/krupd bkp sys" || error=$?; download; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    }; [ ${1} ] || info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
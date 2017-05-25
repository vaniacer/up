#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show updates of server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { echo -e "\nПакеты обновлений:\n"
                 ssh ${addr} "ls ${wdir}/updates/new" || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
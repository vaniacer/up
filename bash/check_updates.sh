#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show updates of server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; do addr

        echo -e "\nПакеты обновлений:\n"
        ssh ${addr} "ls ${wdir}/updates/new" || error=$?

    echo; done; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
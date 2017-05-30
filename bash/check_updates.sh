#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show updates of server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    echo -e "\nПакеты обновлений:\n"
    ssh ${addr} "ls ${wdir}/updates/new" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }

# Test function
#function run () { for server in ${servers}; { addr; for ((i=0; i<10; i++)); { sleep 1
#
#    echo ok
#
#}; }; }; info 'Done' ${error}
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------ #---------------------| Function description |------------------------------------------------
    echo -e "Backup database on server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        ssh ${addr} "${wdir}/krupd bkp db" || error=$?; download

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
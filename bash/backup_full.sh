#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Backup full on server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        ssh ${addr} "${wdir}/krupd bkp db"  || error=$?; download
        ssh ${addr} "${wdir}/krupd bkp sys" || error=$?; download

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
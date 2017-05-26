#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Delete all Updates from Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        ssh ${addr} "echo -e \"Delete files:\n$(ls ${wdir}/updates/new)\""
        ssh ${addr} "rm ${wdir}/updates/new/*" || error=$?

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
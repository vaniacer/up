#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Delete all Updates from Server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh ${addr} "echo -e \"Delete files:\n$(ls ${wdir}/updates/new)\""
    ssh ${addr} "rm ${wdir}/updates/new/*" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
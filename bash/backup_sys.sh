#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Backup system on server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh ${addr} "${wdir}/krupd bkp sys" || error=$?; download

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
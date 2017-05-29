#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Get DB dump from server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh ${addr} "${wdir}/krupd bkp db" || error=$?; download
    ssh ${addr} "rm ${name}" || error=$? # Удаляю файл - ${name}"

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
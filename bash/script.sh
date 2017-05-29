#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Run script(s):\n${updates// /\\n}\n\non Server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    for file in ${updates}; { filename=${file##*/}

        echo -e "\nCopy script - ${filename}"
        scp ${file} ${server}/updates/new || error=$?

        echo -e "Run script - ${filename}\n"
        ssh ${addr} "cd ${wdir}; chmod +x updates/new/${filename}; updates/new/${filename}" || error=$?
        ssh ${addr} "rm ${wdir}/updates/new/${filename}" || error=$?
    }
} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
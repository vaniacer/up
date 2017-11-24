#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Run SQL script(s):\n${scripts// /\\n}\n\non Server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    for file in ${scripts}; { filename=${file##*/}

        echo -e "\nCopy script - ${filename}"
#        scp ${file} ${addr}:${wdir}/updates/new || error=$?
        rsync -e "ssh" --progress -lzuogthvr ${file} ${addr}:${wdir}/updates/new/ || error=$?

        ssh ${addr} "${wdir}/krupd execsql ${wdir}/updates/new/${filename}" || error=$?
        ssh ${addr} "rm ${wdir}/updates/new/${filename}" || error=$?
    }
} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
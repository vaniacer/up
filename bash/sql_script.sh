#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Run SQL script(s):\n${updates// /\\n}\n\non Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr
        for file in ${updates}; { filename=${file##*/}

            echo -e "\nCopy script - ${filename}"
            scp ${file} ${server}/updates/new || error=$?

            ssh ${addr} "${wdir}/krupd execsql ${wdir}/updates/new/${filename}" || error=$?
            ssh ${addr} "rm ${wdir}/updates/new/${filename}" || error=$?; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
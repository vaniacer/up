#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Run SQL script(s):\n${updates// /\\n}\n\non Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { for file in ${updates}; {
                    filename=$(basename ${file})
                    echo -e "\nCopy script - ${filename}"
                    scp ${file} ${server}/updates/new || error=$?

                    ssh ${addr} "${wdir}/krupd execsql ${wdir}/updates/new/${filename}" || error=$?
                    ssh ${addr} "rm ${wdir}/updates/new/${filename}" || error=$?

               }; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
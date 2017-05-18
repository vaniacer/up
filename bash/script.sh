#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Run script(s):\n${updates// /\\n}\n\non Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; do addr

        # Check access
        ssh ${addr} "echo > /dev/null" \
            && { for file in ${updates}; do
                    filename=$(basename ${file})
                    echo -e "\nCopy script - ${filename}"
                    scp ${file} ${server}/updates/new || error=$?

                    echo -e "Run  script - ${filename}\n"
                    ssh ${addr} "cd ${wdir}; chmod +x updates/new/${filename}; updates/new/${filename}" || error=$?
                    ssh ${addr} "rm ${wdir}/updates/new/${filename}" || error=$?

                 echo; done; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; info 'Done'
} #---------------------------------------------------------------------------------------------------------------------
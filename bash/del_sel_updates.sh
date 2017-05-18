#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Delete Update(s):\n${updates// /\\n}\n\nfrom Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; do addr

        # Check access
        ssh ${addr} "echo > /dev/null" \
            && { for file in ${updates}; do
                    filename=$(basename ${file})
                    echo -e "Delete file - ${filename}."
                    ssh ${addr} "rm ${wdir}/updates/new/${filename}" || error=$?

                echo; done; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; info 'Done'
} #---------------------------------------------------------------------------------------------------------------------
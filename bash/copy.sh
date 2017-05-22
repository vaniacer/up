#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Copy Update(s):\n${updates// /\\n}\n\nto Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; do addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { for file in ${updates}; do
                    filename=$(basename ${file})
                    echo -e "\nCopy file - ${filename}"

                    # Check if file exist, copy if not exist
                    ssh ${addr} ls ${wdir}/updates/new/${filename} &> /dev/null \
                        && { echo -e "File - ${filename} exist, skip."; } \
                        || { scp ${file} ${server}/updates/new || error=$?; }

                echo; done; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    echo; done; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
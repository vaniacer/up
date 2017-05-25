#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Delete Update(s):\n${updates// /\\n}\n\nfrom Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { for file in ${updates}; {
                    filename=$(basename ${file})
                    echo -e "Delete file - ${filename}."
                    ssh ${addr} "rm ${wdir}/updates/new/${filename}" || error=$?

               }; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
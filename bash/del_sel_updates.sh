#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Delete Update(s):\n${updates// /\\n}\n\nfrom Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        for file in ${updates}; {
            filename=${file##*/}; echo -e "Delete file - ${filename}."
            ssh ${addr} "rm ${wdir}/updates/new/${filename}" || error=$?; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
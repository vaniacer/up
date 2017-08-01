#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Copy Update(s):\n${updates// /\\n}\n\nto Server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

#    for file in ${updates}; { filename=${file##*/}
#
#        # Check if file exist, copy if not exist
#        ssh ${addr} ls ${wdir}/updates/new/${filename} &> /dev/null \
#            && { echo -e "File - ${filename} exist, skip."; continue; }
#
#        echo -e "Copy file - ${filename}"
##        scp ${file} ${addr}:${wdir}/updates/new/ || error=$?
#        rsync -e "ssh" --progress -lzuogthvr ${file} ${addr}:${wdir}/updates/new/ || error=$?
#    }
    rsync -e "ssh" --progress -lzuogthvr ${updates} ${addr}:${wdir}/updates/new/ || error=$?
} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
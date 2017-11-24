#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Delete Update(s):\n${updates// /\\n}\n\nfrom Server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    for file in $updates; {
        filename=${file##*/}; echo -e "Delete file - $filename."
        ssh $addr "rm $wdir/updates/new/$filename" || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
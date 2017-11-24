#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Copy utils folder to server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $addr [ -d '.utils' ] || ssh $addr mkdir .utils || error=$?
    rsync -e "ssh" --progress -lzuogthvr ~/utils/* $addr:~/.utils || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
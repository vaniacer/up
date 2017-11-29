#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Copy utils folder to server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $sopt $addr [ -d '.utils' ]   ||   ssh $sopt $addr mkdir .utils || error=$?
    rsync -e "ssh $sopt" --progress -lzuogthvr ~/utils/* $addr:~/.utils || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
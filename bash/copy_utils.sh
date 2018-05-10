#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nCopy utils folder to server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    rsync -e "ssh $sopt" --progress -lzghr ~/utils/* $addr:~/.utils || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
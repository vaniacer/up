#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nCopy utils folder to server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    rsync -e "ssh $sopt" --progress -lzghr ~/utils/* $addr:~/.utils || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
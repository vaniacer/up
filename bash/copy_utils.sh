#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nCopy utils folder to server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    rsync -e "ssh -t -t $sopt" --progress -lzghr ~/utils/* $addr:~/.utils || error=$?

} #---------------------------------------------------------------------------------------------------------------------
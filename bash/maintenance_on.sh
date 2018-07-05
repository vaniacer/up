#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nStart dummy page on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    printf "\nStart dummy page\n"
    ssh $sopt $addr "~/.utils/dp.sh --start --jport $port" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
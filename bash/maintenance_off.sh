#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nStop dummy page on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    printf "\nStop dummy page."
    ssh -ttt $sopt $addr '~/.utils/dp.sh --stop' || error=$?

} #---------------------------------------------------------------------------------------------------------------------
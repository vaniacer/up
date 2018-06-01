#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nStop dummy page on server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    printf "\nStop dummy page."
    ssh -ttt $sopt $addr '~/.utils/dp.sh --stop' || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
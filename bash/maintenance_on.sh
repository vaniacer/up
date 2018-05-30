#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nStart dummy page on server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    printf "\nStart dummy page."
    ssh $sopt $addr "~/.utils/dp.sh --start --jport $port" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nDelete all updates from server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    printf "\nDelete all files in $wdir/updates/new)\n"
    ssh -t -t $sopt $addr "rm $wdir/updates/new/*" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
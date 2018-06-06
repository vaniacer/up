#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nDelete all updates from server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -ttt $sopt $addr "echo -e \"\nDelete files:\n$(ls $wdir/updates/new)\""
    ssh -ttt $sopt $addr "rm $wdir/updates/new/*" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
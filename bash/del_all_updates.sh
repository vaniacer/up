#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nDelete all updates from server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh -ttt $sopt $addr "echo -e \"\nDelete files:\n$(ls $wdir/updates/new)\""
    ssh -ttt $sopt $addr "rm $wdir/updates/new/*" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
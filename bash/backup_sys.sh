#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nBackup system on server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh $sopt $addr "$wdir/krupd bkp sys" || error=$?; download

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
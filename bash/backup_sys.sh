#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nBackup system on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -ttt $sopt $addr "$wdir/krupd bkp sys" || error=$?; download

} #---------------------------------------------------------------------------------------------------------------------
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nBackup database on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -ttt $sopt $addr "$wdir/krupd bkp db" || error=$?; download

} #---------------------------------------------------------------------------------------------------------------------
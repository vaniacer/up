#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nBackup full on server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh -ttt $sopt $addr "$wdir/krupd bkp db"  || error=$?; download
    ssh -ttt $sopt $addr "$wdir/krupd bkp sys" || error=$?; download

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
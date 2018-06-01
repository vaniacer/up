#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nRestart jboss on server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh -ttt $sopt $addr $wdir/krupd jboss.stop  || error=$?
    ssh -ttt $sopt $addr $wdir/krupd jboss.start || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
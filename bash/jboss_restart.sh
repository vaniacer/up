#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nRestart jboss on server:\n$addr"
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh $sopt $addr $wdir/krupd jboss.stop  || error=$?
    ssh $sopt $addr $wdir/krupd jboss.start || error=$?

} #---------------------------------------------------------------------------------------------------------------------
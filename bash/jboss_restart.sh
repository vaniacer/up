#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nRestart jboss on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -t -t $sopt $addr $wdir/krupd jboss.stop  || error=$?
    ssh -t -t $sopt $addr $wdir/krupd jboss.start || error=$?

} #---------------------------------------------------------------------------------------------------------------------
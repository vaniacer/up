#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nRestart jboss on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -t -t $sopt $addr $wdir/krupd jboss.stop  || error=$?
    ssh       $sopt $addr $wdir/krupd jboss.start || error=$? # start without -t -t, or it'll drop in the end

} #---------------------------------------------------------------------------------------------------------------------
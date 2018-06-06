#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nStop jboss on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -ttt $sopt $addr $wdir/krupd jboss.stop || error=$?

} #---------------------------------------------------------------------------------------------------------------------
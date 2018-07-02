#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nStart jboss on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -t -t $sopt $addr $wdir/krupd jboss.start || error=$?

} #---------------------------------------------------------------------------------------------------------------------
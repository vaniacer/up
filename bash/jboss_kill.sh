#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nKill jboss on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh $sopt $addr $wdir/krupd jboss.kill || error=$?

} #---------------------------------------------------------------------------------------------------------------------
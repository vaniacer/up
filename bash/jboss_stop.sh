#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nStop jboss on server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh $sopt $addr $wdir/krupd jboss.stop || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
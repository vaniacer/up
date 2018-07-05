#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nReload jboss config on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh $sopt $addr $wdir/jboss-bas-*/bin/jboss-cli.sh -c command=":reload" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
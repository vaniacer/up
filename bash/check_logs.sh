#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow logs of server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -ttt $sopt $addr "cat $wdir/jboss-bas-*/standalone/log/server.log" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
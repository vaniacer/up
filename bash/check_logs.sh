#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow logs of server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh $sopt $addr "cat $wdir/jboss-bas-*/standalone/log/server.log" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
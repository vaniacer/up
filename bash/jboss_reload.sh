#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nReload jboss config on server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh -ttt $sopt $addr $wdir/jboss-bas-*/bin/jboss-cli.sh -c command=":reload" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
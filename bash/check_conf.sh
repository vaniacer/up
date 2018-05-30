#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow conf of server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh $sopt $addr "
        printf '\nJava options\n'
        ps axo command | grep $wdir | grep [j]ava

        printf '\nStandalone-full.xml\n'
        cat $wdir/jboss-bas-*/standalone/configuration/standalone-full.xml" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
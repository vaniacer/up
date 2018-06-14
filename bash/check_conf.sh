#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow conf of server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    # Add server name coz this command not stored in history and don't have event.serv.name
    printf "\n-----{ Server $addr }-----\n"

    ssh -ttt $sopt $addr "
        printf '\nJava options\n'
        ps axo command | grep $wdir | grep [j]ava

        printf '\nStandalone-full.xml\n'
        cat $wdir/jboss-bas-*/standalone/configuration/standalone-full.xml" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
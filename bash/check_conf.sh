#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow conf of server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    # Add server name coz this command not stored in history and don't have event.serv.name
    printf "\n-----{ <b>Server $addr</b> }-----\n"

    ssh $sopt $addr "
        printf '\n<b>Java options</b>\n\n'
        ps axo command | grep $wdir | grep [j]ava

        printf '\n<b>Standalone-full.xml</b>\n\n'
        cat $wdir/jboss-bas-*/standalone/configuration/standalone-full.xml | sed 's|<|\&lt\;|g;s|>|\&gt\;|g'" \
            || error=$?

} #---------------------------------------------------------------------------------------------------------------------
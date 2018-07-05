#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow logs of server:\n$addr"
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    # Add server name coz this command not stored in history and don't have event.serv.name
    printf "\n-----{ <b>Server $addr</b> }-----\n\n"

    ssh $sopt $addr "cat $wdir/jboss-bas-*/standalone/log/server.log" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
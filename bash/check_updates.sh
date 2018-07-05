#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow updates of server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    # Add server name coz this command not stored in history and don't have event.serv.name
    printf "\n-----{ <b>Server $addr</b> }-----\n"

    printf "\nПакеты обновлений:\n"
    ssh $sopt $addr "ls $wdir/updates/new" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
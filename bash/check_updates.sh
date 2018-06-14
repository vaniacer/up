#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow updates of server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    # Add server name coz this command not stored in history and don't have event.serv.name
    printf "\n-----{ Server $addr }-----\n"

    printf "\nПакеты обновлений:\n"
    ssh -ttt $sopt $addr "ls $wdir/updates/new" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
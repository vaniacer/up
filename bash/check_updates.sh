#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nShow updates of server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address and print it in log

    printf "\nПакеты обновлений:\n"
    ssh -ttt $sopt $addr "ls $wdir/updates/new" || error=$?

    info 'Done' $error

} #---------------------------------------------------------------------------------------------------------------------
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    # Put description here. Variables: ${servers[@]}, ${updates[@]}, ${scripts[@]}, ${jobs[@]}, $cmd.
    # This function used(need) to make cron jobs description, to understand what this cron job will do.
    # Example:
    addr > /dev/null
    printf "\nCopy Update(s):\n"; for i in "${updates[@]//\'/}"; { echo "${i##*/}"; }
    printf     "\nto Server):\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -t -t $sopt $addr "Put your code here" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
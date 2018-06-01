#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    # Put description here. Variables: ${servers[@]}, ${updates[@]}, ${scripts[@]}, ${jobs[@]}, $cmd.
    # This function used(need) to make cron jobs description, to understand what this cron job will do.
    # Example:
    addr > /dev/null
    printf "\nCopy Update(s):\n"; for i in "${updates[@]//\'/}"; { echo "${i##*/}"; }
    printf     "\nto Server):\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh -ttt $sopt $addr "Put your code here" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
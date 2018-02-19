#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    # Put description here. Variables: ${servers[@]}, ${updates[@]}, ${scripts[@]}, ${jobs[@]}, $cmd.
    # This function used to make cron jobs description. To understand what this cron job will do.
    # Example:
    printf "\nCopy Update(s):\n"; for i in "${updates[@]}"; { echo "${i##*/}"; }
    printf   "\nto Server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $sopt $addr "Put your code here" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
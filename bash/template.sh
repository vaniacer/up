#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    # Put description here. Variables: "${servers[@]}" $updates $scripts $jobs $cmd. Example:
    printf "Copy Update(s):\n"; for i in "${updates[@]}"; { echo "$i"; }
    printf "\nto Server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $sopt $addr echo "Put your code here" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
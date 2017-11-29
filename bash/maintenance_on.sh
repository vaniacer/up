#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Start dummy page on server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    echo -e "Start dummy page."
    ssh $sopt $addr "~/.utils/dp.sh --start --jport $port" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
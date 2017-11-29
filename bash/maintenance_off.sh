#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Stop dummy page on server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    echo -e "Stop dummy page."
    ssh $sopt $addr '~/.utils/dp.sh --stop' || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
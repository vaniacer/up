#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nShow updates of server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    echo -e "\nПакеты обновлений:\n"
    ssh $sopt $addr "ls $wdir/updates/new" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
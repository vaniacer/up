#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Delete Update(s):\n"; for i in "${updates[@]}"; { echo "$i"; }
    printf "\nfrom Server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    for file in "${updates[@]}"; {
        filename=${file##*/}; echo -e "Delete file - $filename."
        ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nDelete Update(s):\n"; for i in "${updates[@]}"; { echo "${i##*/}"; }
    printf "\nfrom Server(s):\n";   for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    printf "\n"
    for file in "${updates[@]}"; {
        filename=${file##*/}; echo -e "\nDelete file - $filename."
        ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
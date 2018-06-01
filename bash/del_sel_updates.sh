#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nDelete Update(s):\n"; for i in "${updates[@]//\'/}"; { echo "${i##*/}"; }
    printf      "\nfrom Server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    for file in "${updates[@]}"; {
        filename=${file##*/}; echo -e "\nDelete file - $filename."
        ssh -ttt $sopt $addr "rm $wdir/updates/new/$filename" || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
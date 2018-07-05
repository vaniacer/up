#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nDelete Update(s):\n"; for i in "${updates[@]//\'/}"; { echo "${i##*/}"; }
    printf      "\nfrom Server:\n$addr"
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    for file in "${updates[@]}"; {
        filename=${file##*/}
        printf "\nDelete file - $filename\n"
        ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------
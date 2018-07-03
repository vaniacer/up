#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nCopy Update(s):\n"; for i in "${updates[@]//\'/}"; { echo "${i%%:*}"; }
    printf      "\nto Server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    rsync -e "ssh $sopt" --progress -lzuogthvr "${updates[@]}" $addr:$wdir/updates/new/ || error=$?

} #---------------------------------------------------------------------------------------------------------------------
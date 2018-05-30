#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nCopy Update(s):\n"; for i in "${updates[@]//\'/}"; { echo "${i%%:*}"; }
    printf      "\nto Server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    rsync -e "ssh $sopt" --progress -lzuogthvr "${updates[@]}" $addr:$wdir/updates/new/ || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
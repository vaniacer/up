#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nCopy Update(s):\n"; for i in "${updates[@]}"; { echo "${i%%:*}"; }
    printf "\nto Server(s):\n";   for i in "${servers[@]}"; { echo "${i##*/}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    printf "\n"
    rsync -e "ssh $sopt" --progress -lzuogthvr "${updates[@]}" $addr:$wdir/updates/new/ || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
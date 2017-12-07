#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Copy DB dump $updates to server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    filename=$dumps

    printf "\nCopy dump.\n"
    rsync -e "ssh $sopt" --progress -lzuogthvr "$dumpdir/$pname/$dumps" $addr:$wdir/updates/new/ && {

        ssh $sopt $addr "cd $wdir; ./krupd restore db updates/new/$filename" || error=$?
        ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?

    } || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () {

    [[ ${#dumps[*]} -gt 1 ]] && { printf "\nMultiple dumps selected, need one.\n"; error=1; } || {

        for server in "${servers[@]}"; { addr; body; }; info 'Done' $error

    }
}
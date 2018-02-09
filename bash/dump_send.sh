#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Copy DB dump $updates to server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    filename=$dumps
    attention=(
       '     _  _____ _____ _____ _   _ _____ ___ ___  _   _ _ \n'
        "   / \|_   _|_   _| ____| \ | |_   _|_ _/ _ \| \ | | |\n"
        "  / _ \ | |   | | |  _| |  \| | | |  | | | | |  \| | |\n"
        " / ___ \| |   | | | |___| |\  | | |  | | |_| | |\  |_|\n"
        "/_/   \_\_|   |_| |_____|_| \_| |_| |___\___/|_| \_(_)\n")

    echo -e "<b>${attention[@]}</b>\n"
    printf "You are sending dump - <b>$filename</b>\n"
    printf "to server - <b>$addr</b>\n\n"

    printf "If it's not what you wished to do you've got <b>30</b> seconds to cancel this!\n"
    printf "Final countdown...\n"
    for i in {1..30}; { sleep 1; echo $i; }
    printf "Ok, i warned you!)\n"

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
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Run SQL script(s):\n"; for i in "${scripts[@]}"; { echo "$i"; }
    printf    "\non Server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    for file in "${scripts[@]}"; { filename=${file##*/}

        # Copy script to server
        rsync -e "ssh $sopt" --progress -lzuogthvr $file $addr:$wdir/updates/new/ > /dev/null && {

            # Run script
            ssh $sopt $addr "$wdir/krupd execsql $wdir/updates/new/$filename" || error=$?

            # Delete script after execution
            ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?

        } || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
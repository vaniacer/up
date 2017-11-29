#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Run SQL script(s):\n"; for i in "${scripts[@]}"; { echo "$i"; }
    printf    "\non Server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    for file in "${scripts[@]}"; { filename=${file##*/}

        echo -e "\nCopy script - $filename"
        rsync -e"ssh $sopt" --progress -lzuogthvr $file $addr:$wdir/updates/new/ || error=$?

        ssh $sopt $addr "$wdir/krupd execsql $wdir/updates/new/$filename" || error=$?
        ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
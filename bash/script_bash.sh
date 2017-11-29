#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf  "Run script(s):\n"; for i in "${scripts[@]}"; { echo "$i"; }
    printf "\non Server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    for file in "${scripts[@]}"; { filename=${file##*/}

        printf "\nCopy script - $filename\n"
        rsync -e "ssh $sopt" --progress -lzuogthvr $file $addr:$wdir/updates/new/ || error=$?

        printf "\nRun  script - $filename\n"
        ssh $sopt $addr "cd $wdir; chmod +x updates/new/$filename; updates/new/$filename" || error=$?

        printf "\nDelete script - $filename\n"
        ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
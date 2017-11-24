#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Run script(s):\n${scripts// /\\n}\n\non Server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    for file in $scripts; { filename=${file##*/}

        printf "\nCopy script - $filename\n"
        rsync -essh --progress -lzuogthvr $file $addr:$wdir/updates/new/ || error=$?

        printf "Run  script - $filename\n"
        ssh $addr "cd $wdir; chmod +x updates/new/$filename; updates/new/$filename" || error=$?

        printf "\nDelete script - $filename\n"
        ssh $addr "rm $wdir/updates/new/$filename" || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Copy Update(s):\n${updates// /\\n}\n\nto Server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    rsync -e "ssh" --progress -lzuogthvr $updates $addr:$wdir/updates/new/ || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
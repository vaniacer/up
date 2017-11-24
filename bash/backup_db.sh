#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Backup database on server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $addr "$wdir/krupd bkp db" || error=$?; download

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
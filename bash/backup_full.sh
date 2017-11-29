#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Backup full on server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $sopt $addr "$wdir/krupd bkp db"  || error=$?; download
    ssh $sopt $addr "$wdir/krupd bkp sys" || error=$?; download

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
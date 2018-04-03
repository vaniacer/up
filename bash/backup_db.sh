#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nBackup database on server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    printf "\n"
    ssh $sopt $addr "$wdir/krupd bkp db" || error=$?; download

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
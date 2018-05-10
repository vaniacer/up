#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nBackup system on server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh $sopt $addr "$wdir/krupd bkp sys" || error=$?; download

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nDelete all updates from server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh $sopt $addr "echo -e \"\nDelete files:\n$(ls $wdir/updates/new)\""
    ssh $sopt $addr "rm $wdir/updates/new/*" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
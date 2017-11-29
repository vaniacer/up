#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Delete all updates from server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $sopt $addr "echo -e \"Delete files:\n$(ls $wdir/updates/new)\""
    ssh $sopt $addr "rm $wdir/updates/new/*" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
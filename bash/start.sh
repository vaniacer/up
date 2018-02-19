#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nStart server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    printf "\n"
    ssh $sopt $addr $wdir/krupd jboss.start || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
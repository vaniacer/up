#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nStart server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh $sopt $addr $wdir/krupd jboss.kill || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
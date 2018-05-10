#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nShutdown server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh $sopt $addr $wdir/krupd jboss.stop || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
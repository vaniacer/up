#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nShow logs of server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    printf "\n"
    ssh $sopt $addr "cat $wdir/jboss-bas-*/standalone/log/server.log" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nReload config on server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    printf "\n"
    ssh $sopt $addr $wdir/jboss-bas-*/bin/jboss-cli.sh -c command=":reload" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
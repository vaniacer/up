#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Show logs of server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $sopt $addr "cat $wdir/jboss-bas-*/standalone/log/server.log" || error=$?
    ssh $sopt $addr  "ls $wdir/jboss-bas-*/standalone/log | grep $(date +'%Y-%m-%d')" \
        && { ssh $sopt $addr "cat $wdir/jboss-bas-*/standalone/log/server.log.$(date +'%Y-%m-%d')*" || error=$?; }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show logs of server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $addr "cat $wdir/jboss-bas-*/standalone/log/server.log" || error=$?
    ssh $addr  "ls $wdir/jboss-bas-*/standalone/log | grep $(date +'%Y-%m-%d')" \
        && { ssh $addr "cat $wdir/jboss-bas-*/standalone/log/server.log.$(date +'%Y-%m-%d')*" || error=$?; }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
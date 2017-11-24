#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Restart server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $addr $wdir/krupd jboss.stop  || error=$?
    ssh $addr $wdir/krupd jboss.start || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
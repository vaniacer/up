#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Reload config on server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $addr $wdir/jboss-bas-*/bin/jboss-cli.sh -c command=":reload" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
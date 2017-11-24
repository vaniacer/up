#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show conf of server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $addr "
        echo -e '\nJava options\n'
        ps axo command | grep $wdir | grep [j]ava

        echo -e '\nStandalone-full.xml\n'
        cat $wdir/jboss-bas-*/standalone/configuration/standalone-full.xml" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
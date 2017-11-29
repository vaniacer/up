#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Show conf of server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $sopt $addr "
        echo -e '\nJava options\n'
        ps axo command | grep $wdir | grep [j]ava

        echo -e '\nStandalone-full.xml\n'
        cat $wdir/jboss-bas-*/standalone/configuration/standalone-full.xml" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
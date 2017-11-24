#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Start dummy page on server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    echo -e "Start dummy page."
    ssh $addr "~/.utils/dp.sh --start --jport $port" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Stop dummy page on server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    echo -e "Stop dummy page."
    ssh ${addr} '~/.utils/dp.sh --stop' || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
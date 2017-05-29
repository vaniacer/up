#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Copy utils folder to server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh ${addr} [ -d '.utils' ] || mkdir .utils || error=$?
    scp -r ~/utils/* ${addr}:~/.utils || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
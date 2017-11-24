#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    # Put description here. Variables: $servers $updates $scripts $jobs $cmd. Example:
    echo -e "Copy Update(s):\n${updates// /\\n}\n\nto Server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $addr echo "Put your code here" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
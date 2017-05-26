#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Put description here. Variables: ${servers} ${updates} ${jobs} ${cmd}. Example:
    Copy Update(s):\n${updates// /\\n}\n\nto Server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        ssh ${addr} echo "Put your code here" || error=$?

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
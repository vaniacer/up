#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Copy utils folder to server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        ssh ${addr} [ -d '.utils' ] || mkdir .utils || error=$?
        scp -r ~/utils/* ${addr}:~/.utils || error=$?

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
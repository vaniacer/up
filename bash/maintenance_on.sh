#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Start dummy page on server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        echo -e "Start dummy page."
        ssh ${addr} '~/.utils/dp.sh --start' || error=$?

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
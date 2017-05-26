#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Stop dummy page on server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        echo -e "Stop dummy page."
        ssh ${addr} '~/.utils/dp.sh --stop' || error=$?

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
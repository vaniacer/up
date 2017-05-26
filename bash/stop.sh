#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Shutdown server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        ssh ${addr} ${wdir}/krupd jboss.stop || error=$?

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
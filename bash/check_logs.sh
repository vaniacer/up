#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show logs of server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        ssh ${addr} "cat ${wdir}/jboss-bas-*/standalone/log/server.log" || error=$?

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
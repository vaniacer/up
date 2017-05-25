#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show conf of server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { ssh  ${addr} "cat ${wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml" || error=$?; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
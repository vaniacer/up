#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show conf of server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        ssh ${addr} "cat ${wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml" || error=$?

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
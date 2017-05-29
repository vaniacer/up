#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show conf of server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh ${addr} "cat ${wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
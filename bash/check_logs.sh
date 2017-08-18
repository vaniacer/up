#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Show logs of server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh ${addr} "cat ${wdir}/jboss-bas-*/standalone/log/server.log \
    ${wdir}/jboss-bas-*/standalone/log/*$(date +'%Y-%m-%d')" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
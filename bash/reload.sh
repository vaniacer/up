#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Reload config on server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        ssh ${addr} ${wdir}/jboss-bas-*/bin/jboss-cli.sh -c command=":reload" || error=$?

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Make ssh tunnel to server's port."; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    lport=42250
    rport=8080

    until ! netstat -ln | grep ${lport} > /dev/null; do ((lport++)); done
    echo -e "\n<a class=\"btn btn-primary\" href=\"http://__URL__:${lport}/login\">Connect</a>\n"
    ssh ${addr} -f -L 0.0.0.0:${lport}:127.0.0.1:${rport} sleep 10

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
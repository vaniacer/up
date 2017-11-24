#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Make ssh tunnel to server's port."; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    timer=60
    lport=42250     #42250
    rport=${port}   #8080

    until ! netstat -ln | grep $lport > /dev/null; do ((lport++)); done
    echo -e "\n<a class=\"btn btn-primary\" href=\"http://__URL__:$lport/application\">Application</a>\n"
    echo -e "\n<a class=\"btn btn-primary\" href=\"http://__URL__:$lport\">Connect</a>\n"
    echo -e "\n<a class=\"btn btn-primary\" href=\"http://__URL__:$lport/login\">Login</a>\n"
    ssh $addr -f -L 0.0.0.0:$lport:127.0.0.1:$rport sleep $timer || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
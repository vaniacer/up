#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake ssh tunnel to server's port."
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    # Add server name coz this command not stored in history and don't have event.serv.name
    printf "\n-----{ <b>Server $addr</b> }-----\n"

    timer=60      # If not used, connection will be dropped after this amount of seconds
    lport=42250   # default 42250
    rport=${port} # default 8080

    postfixes=('/application' '/login' '')

    until ! netstat -ln | grep $lport > /dev/null; do ((lport++)); done
    for postfix in "${postfixes[@]}"; {
        printf "\n<a href=\"http://__URL__:$lport$postfix\">http://__URL__:$lport$postfix</a>\n"
    }
    ssh -t -t $sopt $addr -f -L 0.0.0.0:$lport:127.0.0.1:$rport sleep $timer || error=$?

} #---------------------------------------------------------------------------------------------------------------------
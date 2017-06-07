#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Make ssh tunnel to server's port."; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    lport=10100
    rport=8080
    inter=($(ip a | grep 'inet ' | sed '/127.0.0.1/d; s/.*inet //g; s|/.*$||g'))

    until ! netstat -ln | grep ${lport} > /dev/null; do ((lport++)); done
    for i in ${inter[@]}; { printf "\n<a class='btn btn-primary' href='http://${i}:${lport}/login'>Connect</a>\n"; }
    ssh ${addr} -f -L 0.0.0.0:${lport}:127.0.0.1:${rport} sleep 10


} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in ${servers}; { addr; body; }; info 'Done' ${error}; }
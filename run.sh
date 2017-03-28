#!/bin/bash

addr=localhost
port=8000
pidf=/tmp/gpid

help="
Available options are:
    -addr  | -a  Bind address(localhost).
    -port  | -p  Bind port(8000).
    -kill  | -k  Stop server.
    -help  | -h  This message.
    -reset | -r  Restart server.

Usage:
    # Simple start
    ./$(basename $0)

    # Change bind address and port
    ./$(basename $0) -a 192.168.0.1 -p 9000

    # Kill
    ./$(basename $0) -k
"

function start {
    source ../env/bin/activate
    gunicorn ups.wsgi --error-logfile ../logs/error --log-file ../logs/log --access-logfile ../logs/access \
             --pid ${pidf} --daemon --bind ${addr}:${port} --graceful-timeout 600 --timeout 600
}

function stop {
    [ -e ${pidf} ] && { kill $(cat ${pidf}); rm ${pidf}; }
}

function reset {
    stop
    start
}

#Get opts
until [ -z "$1" ]; do case $1 in

    -addr  | -a) shift; addr=${1};;
    -port  | -p) shift; port=${1};;
    -kill  | -k) starter=kill;;
    -reset | -r) starter=reset;;
    -help  | -h) echo -e "${help}"; exit 0;;
              *) echo -e "Unknown option - ${1}"; exit 1;;

esac; shift; done

case ${starter} in
    kill ) stop;;
    reset) reset;;
        *) start;;
esac
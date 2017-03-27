#!/bin/bash

host=localhost
port=8000


function start {
    source ../env/bin/activate
    gunicorn ups.wsgi --log-file ../log --pid ../pid \
             --daemon --bind ${host}:${port} --graceful-timeout 600 --timeout 600
}

function stop {
    kill $(cat ../pid)
}

function reset {
    stop
    start
}

#Get opts
until [ -z "$1" ]; do case $1 in

    -host  | -h) shift; host=${1};;
    -port  | -p) shift; port=${1};;
    -kill  | -k) stop;;
    -reset | -r) reset;;

esac; shift; done

start
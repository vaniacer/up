#!/bin/bash

host=localhost
port=8000
pidf=/tmp/gpid

function start {
    source ../env/bin/activate
    gunicorn ups.wsgi --error-logfile ../logs/error --log-file ../logs/log --access-logfile ../logs/access \
             --pid ${pidf} --daemon --bind ${host}:${port} --graceful-timeout 600 --timeout 600
}

function stop {
    kill $(cat ${pidf})
}

function reset {
    stop
    start
}

[ "$@" ] || start

#Get opts
until [ -z "$1" ]; do case $1 in

    -host  | -h) shift; host=${1};;
    -port  | -p) shift; port=${1};;
    -kill  | -k) stop;;
    -reset | -r) reset;;

esac; shift; done
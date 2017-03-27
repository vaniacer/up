#!/bin/bash

host=localhost
port=8000

#Get opts
until [ -z "$1" ]; do case $1 in

    -host | -h) shift; host=${1};;
    -port | -p) shift; port=${1};;
    -kill | -k) kill=true;;

esac; shift; done

[ ${kill} ] && {
        kill $(cat ../pid)
          } || {
        source ../env/bin/activate
        gunicorn ups.wsgi --log-file ../log --pid ../pid --daemon --bind ${host}:${port}
}

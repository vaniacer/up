#!/bin/bash

addr=localhost
port=8000
pidf=/tmp/gpid
daem=--daemon
logd=../logs/
acsf=access
errf=error
logf=log
time=600

#-----------------------------------------------------------------------------------------------------------------------
[ -f run.conf ] && . run.conf

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

function conf {
cat > run.conf << EOF
addr=${addr}
port=${port}
pidf=${pidf}
daem=${daem}
logd=${logd}
acsf=${acsf}
errf=${errf}
logf=${logf}
time=${time}
EOF
}

function start {
    . ../env/bin/activate
    gunicorn ups.wsgi --error-logfile ${logd}${errf} --log-file ${logd}${logf} --access-logfile ${logd}${acsf} \
             --pid ${pidf} --bind ${addr}:${port} --graceful-timeout ${time} --timeout ${time} ${daem} && { conf; }
}

function stop {
    [ -e ${pidf} ] && { kill $(cat ${pidf}); rm ${pidf}; }
}

function reset {
    stop
    start
}

# Get opts
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
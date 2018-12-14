#!/bin/bash

#-----------------------| Default options |-----------------------------------------------------------------------------
wdir=$(dirname $0)      # Get working dir
addr=localhost          # Bind address
port=8000               # Bind port
pidf=/tmp/gpid          # Pid file
daem=--daemon           # Daemon mode
logd=$wdir/../logs/srv/ # Logs dir
acsf=access             # Access log filename(in logs dir)
errf=error              # Error log filename(in logs dir)
logf=log                # Main log filename(in logs dir)
time=600                # Timeout in sec
grce=10                 # Graceful timeout in sec
work=5                  # Number of workers
#-----------------------------------------------------------------------------------------------------------------------
[[ -f $wdir/run.conf ]] && . $wdir/run.conf # get saved conf if exist

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
    . $wdir/../env/bin/activate
    gunicorn ups.wsgi                \
             --pid ${pidf}            \
             --workers ${work}         \
             --timeout ${time}          \
             --bind ${addr}:${port}      \
             --log-file ${logd}${logf}    \
             --graceful-timeout ${grce}    \
             --error-logfile ${logd}${errf} \
             --access-logfile ${logd}${acsf} \
             ${daem}
}

function stop {
    [ -e ${pidf} ] && { kill $(cat ${pidf}); rm ${pidf}; }
}

function reset {
    stop
    start
}

# Get opts
until [[ -z "$1" ]]; do case $1 in

    -addr  | -a) shift; addr=${1};;
    -port  | -p) shift; port=${1};;
    -kill  | -k) starter=kill ;;
    -reset | -r) starter=reset;;
    -help  | -h) echo -e "${help}"; exit 0;;
              *) echo -e "Unknown option - ${1}"; exit 1;;

esac; shift; done

case ${starter} in
    kill ) stop;;
    reset) reset;;
        *) start;;
esac
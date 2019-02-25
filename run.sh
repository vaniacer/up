#!/bin/bash

#-----------------------| Default options |-----------------------------------------------------------------------------
wdir=$(dirname $0)      # Get working dir
name=$(basename $0)     # Get script name
addr=localhost          # Bind address
port=8000               # Bind port
pidf=/tmp/gpid          # Pid file
daem=--daemon           # Daemon mode
logd=$wdir/../logs/srv  # Logs dir
acsf=access             # Access log filename(in logs dir)
errf=error              # Error log filename(in logs dir)
logf=log                # Main log filename(in logs dir)
logl=error              # Error log level. Valid level names are: debug, info, warning, error, critical
time=600                # Timeout in sec
grce=10                 # Graceful timeout in sec
work=5                  # Number of workers
#-----------------------------------------------------------------------------------------------------------------------
[[ -f $wdir/run.conf ]] && . $wdir/run.conf # get conf from file if exist

help="
Available options are:
    -addr  | -a  Bind address(localhost).
    -port  | -p  Bind port(8000).
    -kill  | -k  Stop server.
    -help  | -h  This message.
    -reset | -r  Restart server.

Usage:
    # Simple start
    ./$name

    # Change bind address and port
    ./$name -a 192.168.0.1 -p 9000

    # Kill
    ./$name -k
"

function start {
    . $wdir/../env/bin/activate
    gunicorn ups.wsgi            \
             --pid $pidf          \
             --workers $work       \
             --timeout $time        \
             --log-level $logl       \
             --bind $addr:$port       \
             --log-file $logd$logf     \
             --graceful-timeout $grce   \
             --error-logfile $logd/$errf \
             --access-logfile $logd/$acsf \
             $daem
}

function stop {
    [[ -e $pidf ]] && { kill $(cat $pidf); rm $pidf; }
}

function reset {
    stop
    start
}

starter=start

# Get opts
until [[ -z "$1" ]]; do case $1 in

    -addr  | -a) shift; addr=$1;;
    -port  | -p) shift; port=$1;;
    -kill  | -k) starter=stop  ;;
    -reset | -r) starter=reset ;;
    -help  | -h) printf "$help"; exit;;
              *) printf "Unknown option - $1"; exit 1;;

esac; shift; done

$starter
#!/bin/bash

addr=localhost  # Bind address
port=8000       # Bind port
pidf=/tmp/gpid  # Pid file
daem=--daemon   # Daemon mode
logd=../logs/   # Logs dir
acsf=access     # Access log filename(in logs dir)
errf=error      # Error log filename(in logs dir)
logf=log        # Main log filename(in logs dir)
time=600        # Timeout in sec
grce=10         # Graceful timeout in sec
work=5          # Number of workers

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
addr=${addr}$(echo -e '\t')# Bind address
port=${port}$(echo -e '\t\t')# Bind port
pidf=${pidf}$(echo -e '\t\t')# Pid file
daem=${daem}$(echo -e '\t\t')# Daemon mode
logd=${logd}$(echo -e '\t\t')# Logs dir
acsf=${acsf}$(echo -e '\t\t')# Access log filename(in logs dir)
errf=${errf}$(echo -e '\t\t')# Error log filename(in logs dir)
logf=${logf}$(echo -e '\t\t')# Main log filename(in logs dir)
time=${time}$(echo -e '\t\t')# Timeout in sec
grce=${grce}$(echo -e '\t\t\t')# Graceful timeout in sec
work=${work}$(echo -e '\t\t\t')# Number of workers
EOF
}

function start {
    . ../env/bin/activate
    gunicorn ups.wsgi                \
             --pid ${pidf}            \
             --workers ${work}         \
             --timeout ${time}          \
             --bind ${addr}:${port}      \
             --log-file ${logd}${logf}    \
             --graceful-timeout ${grce}    \
             --error-logfile ${logd}${errf} \
             --access-logfile ${logd}${acsf} \
             ${daem} && { conf; }
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
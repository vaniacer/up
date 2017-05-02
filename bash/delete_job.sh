#!/bin/bash

set -e
# Get options and functions
workdir=$(dirname $0)
crondir=${workdir}/../../logs/cron
rundir=${workdir}/../../logs/run
cronfile=/var/spool/cron/crontabs/${USER}
#----------|Get opts|------------
until [ -z "$1" ]; do case $1 in

    -server | -s) servers=${2};;
    -update | -u) updates=${2};;
    -date   | -d) date=${2};;
    -cron   | -C) cron=${2};;
    -desc   | -D) desc=${2};;
    -job    | -j) jobs=${2};;
    -cmd    | -c) cmd=${2};;
    -key    | -k) key=${2};;
    -id     | -i) id=${2};;

esac; shift 2; done
#--------------------------------

for id in ${jobs}; do
    rule="/${id}/d;"${rule}
    echo -e "Отменяю задачу: ${id}"
done

sed "${rule}" -i /var/spool/cron/crontabs/${USER}
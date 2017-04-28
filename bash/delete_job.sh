#!/bin/bash

set -e

#----------|Get opts|------------
until [ -z "$1" ]; do case $1 in

    -server | -s) servers=${2};;
    -update | -u) updates=${2};;
    -job    | -j) jobs=${2};;

esac; shift 2; done
#--------------------------------

for id in ${jobs}; do
    rule="/${id}/d;"${rule}
    echo -e "Отменяю задачу: ${id}"
done

sed "${rule}" -i /var/spool/cron/crontabs/${USER}
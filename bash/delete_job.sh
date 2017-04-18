#!/bin/bash

set -e

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) servers=${2};;
	    -update | -u) updates=${2};;
	    -job    | -j) jobs=${2};;
    esac

    shift 2
done

echo -e "Отменяю задачи в кроне.\n"
for id in ${jobs}; do
    echo ${id}
    rule="/${id}/d;"${rule}

done

sed "${rule}" -i /var/spool/cron/crontabs/${USER}
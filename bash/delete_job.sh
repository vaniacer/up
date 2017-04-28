#!/bin/bash

set -e
# Get options and functions
. $(dirname $0)/func.sh

for id in ${jobs}; do
    rule="/${id}/d;"${rule}
    echo -e "Отменяю задачу: ${id}"
done

sed "${rule}" -i /var/spool/cron/crontabs/${USER}
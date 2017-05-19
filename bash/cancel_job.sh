#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Delete cron job(s):\n${jobs// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    info 'Cancel jobs'
    for id in ${jobs}; do
        rule="/${id}/d;"${rule}
        echo "${id}"
    done

    sed "${rule}" -i /var/spool/cron/crontabs/${USER} || error=$?
    info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
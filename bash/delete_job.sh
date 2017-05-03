#!/bin/bash

function description () {
    echo -e "Delete cron job(s):\n${jobs// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    for id in ${jobs}; do
        rule="/${id}/d;"${rule}
        echo -e "Отменяю задачу: ${id}"
    done

    sed "${rule}" -i /var/spool/cron/crontabs/${USER}
    echo -e "\nDone."
} #---------------------------------------------------------------------------------------------------------------------
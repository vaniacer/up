#!/bin/bash

function run () { #----------------------------------|Main function|----------------------------------------------------
    echo '' > ${rundir}/err${key}
    for id in ${jobs}; do
        rule="/${id}/d;"${rule}
        echo -e "Отменяю задачу: ${id}"
    done

    sed "${rule}" -i /var/spool/cron/crontabs/${USER}

    echo -e "\nDone.\nERROR: ${error}"
    echo ${error} > ${rundir}/err${key}
} #---------------------------------------------------------------------------------------------------------------------
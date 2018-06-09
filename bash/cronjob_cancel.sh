#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nDelete cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    printf "\nCancel job $job_id\n"

    sed "/$job_id/d" -i /var/spool/cron/crontabs/$USER || error=$?

} #---------------------------------------------------------------------------------------------------------------------
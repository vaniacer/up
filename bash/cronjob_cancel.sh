#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nCancel cron job $job_id\n"
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    printf "\nCancel job $job_id\n"

    sed "/$job_id/d" -i /var/spool/cron/crontabs/$USER || error=$?

} #---------------------------------------------------------------------------------------------------------------------
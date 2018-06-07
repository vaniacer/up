#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    printf "\nSet job $job_id to run everyday\n"
    sed "s|;.*$job_id.*$||g;/.*$job_id/ s| [0-9][0-9] [0-9][0-9] \*| \* \* \*|g" -i $cronfile || error=$?

} #---------------------------------------------------------------------------------------------------------------------
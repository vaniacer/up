#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nDelete cron job(s):\n"; for i in "${jobs[@]}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    info 'Cancel jobs'
    for id in "${jobs[@]}"; { rule="/$id/d;"$rule; printf "\n$id"; }
    sed "$rule" -i /var/spool/cron/crontabs/$USER || error=$?
    info 'Done' $error
} #---------------------------------------------------------------------------------------------------------------------
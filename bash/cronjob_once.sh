#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    info 'Set jobs to run once'
    for id in "${jobs[@]}"; {
        rule="s|^.*$id.*$|&; sed \"/$id/d\" -i /var/spool/cron/crontabs/$USER|g;"$rule; echo "$id"
    }

    sed "$rule" -i /var/spool/cron/crontabs/$USER || error=$?
    info 'Done' $error
} #---------------------------------------------------------------------------------------------------------------------
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    info 'Set jobs permanent'
    for id in "${jobs[@]}"; {
        rule="s|;.*$id.*$||g;/.*$id/ s| [0-9][0-9] [0-9][0-9] \*| \* \* \*|g;"$rule; printf "\n$id"
    }
    sed "$rule" -i /var/spool/cron/crontabs/$USER || error=$?
    info 'Done' $error
} #---------------------------------------------------------------------------------------------------------------------
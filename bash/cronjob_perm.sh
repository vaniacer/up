#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Make permanent cron job(s):\n"; for i in "${jobs[@]}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    info 'Set jobs permanent'
    for id in "${jobs[@]}"; { rule="s|;.*$id.*$||g;"$rule; echo "$id"; }
    sed "$rule" -i /var/spool/cron/crontabs/$USER || error=$?
    info 'Done' $error
} #---------------------------------------------------------------------------------------------------------------------
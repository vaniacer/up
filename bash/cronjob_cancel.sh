#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nDelete cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    printf "\nCancel job(s):\n"
    for id in "${jobs[@]}"; { rule="/$id/d;"$rule; printf "$id\n"; }
    sed "$rule" -i /var/spool/cron/crontabs/$USER || error=$?

} #---------------------------------------------------------------------------------------------------------------------
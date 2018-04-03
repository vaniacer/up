#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nChange jobs date\time:\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    # Get time
    time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}
    date="$mm $hh $DD $MM" # Cron format date

    info 'Change job(s) date and time'
    for id in "${jobs[@]}"; {
        job="`grep "\-C $id" /var/spool/cron/crontabs/$USER`"
        job=( ${job//'*'/'\*'} )
        rule="s|${job[@]}|$date ${job[@]:4}|g;"$rule; printf "\n$id"
    }

    sed "$rule" -i /var/spool/cron/crontabs/$USER || error=$?
    info 'Done' $error
} #---------------------------------------------------------------------------------------------------------------------
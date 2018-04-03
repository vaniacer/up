#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nChange jobs date\time:\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    # Get time
    time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}
    date="$mm $hh $DD $MM" # Cron format date

    info 'Change job(s) date and time'
    for id in ${jobs[@]}; {
        job="`grep "\-C $id" $cronfile`"
        job=( ${job//'*'/'\*'} )
        sed="s|${job[@]}|$date ${job[@]:4}|g;"$sed; printf "\n$id"
    }

    sed "$sed" -i $cronfile || error=$?
    info 'Done' $error
} #---------------------------------------------------------------------------------------------------------------------
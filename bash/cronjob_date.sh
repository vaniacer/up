#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nChange jobs date\time:\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    # Get time
    time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}
    date="$mm $hh $DD $MM" # Cron format date

    printf "\nChange run date and time for job $job_id\n"

    job="`grep "\-C $job_id" $cronfile`"
    job="${job//'*'/'\*'}"
    job="${job//-/'\-'}"
    cut=( $job )
    sed="s|^.*-C $id.*$|$date ${cut[@]:4}|g"

    sed "$sed" -i $cronfile || error=$?

} #---------------------------------------------------------------------------------------------------------------------
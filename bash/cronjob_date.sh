#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nChange jobs date\time:\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    printf "\nChange run date and time for job $job_id\n"

    # Get time
    time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}

    job="`grep "\-C $job_id" $cronfile`" # Get cron string
    job="${job//'*'/'\*'}"               # Screen * with \
    job="${job//-/'\-'}"                 # Screen - with \
    cut=( $job )                         # Make an array
    new="$mm $hh $DD $MM ${cut[@]:4}"    # New cron string
    sed="/\-C $job_id/c$new"             # Make sed rule, change cron string with '-C $job_id' to $new string

    sed "$sed" -i $cronfile || error=$?

} #---------------------------------------------------------------------------------------------------------------------
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    printf "\nSet job $job_id to run once\n"

    # Get time
    date=${date% *}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}

    job="`grep "\-C $job_id" $cronfile`"   # Get cron string
    job="${job//'*'/'\*'}"                 # Screen * with \
    job="${job//-/'\-'}"                   # Screen - with \
    cut=( $job )                           # Make an array
    cncl="sed '/$job_id/d' -i '$cronfile'" # Command to delete executed cron job
    cut[2]="$DD"; cut[3]="$MM"             # Set month and day
    new="${cut[@]} ; $cncl"                # New cron string
    sed="/\-C $job_id/c$new"               # Make sed rule, change cron string with '-C $job_id' to $new string

    sed "$sed" -i $cronfile || error=$?

} #---------------------------------------------------------------------------------------------------------------------
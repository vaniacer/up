#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    printf "\nSet job $job_id to run everyday\n"

    job="`grep "\-C $job_id" $cronfile`" # Get cron string
    job="${job//'*'/'\*'}"               # Screen * with \
    job="${job//-/'\-'}"                 # Screen - with \
    cut=( $job )                         # Make an array
    cut[2]='\*'; cut[3]='\*'             # Change month and day to \*
    new="${cut[@]::${#cut[@]}-5}"        # New cron string
    sed="/\-C $job_id/c$new"             # Make sed rule, change cron string with '-C $job_id' to $new string

    sed "$sed" -i $cronfile || error=$?

} #---------------------------------------------------------------------------------------------------------------------
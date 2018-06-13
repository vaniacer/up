#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake cron job $job_id run everyday.\n"
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    printf "\nSet job $job_id to run everyday\n"

    job="`grep "\-C $job_id" $cronfile`" # Get cron string
    job="${job//'*'/'\*'}"               # Screen * with \
    job="${job//-/'\-'}"                 # Screen - with \
    job="${job%%;*}"                     # Cut cancel command
    cut=( $job )                         # Make an array
    cut[2]='\*'; cut[3]='\*'             # Change month and day to \*
    sed="/\-C $job_id/c${cut[@]}"        # Make sed rule, change cron string with '-C $job_id' to $new string

    sed "$sed" -i $cronfile || error=$?

} #---------------------------------------------------------------------------------------------------------------------
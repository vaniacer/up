#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    info 'Set jobs to run once'
    for id in "${jobs[@]}"; {
        sed="s|^.*$id.*$|&; sed \"/$id/d\" -i $cronfile|g;"$sed; printf "\n$id"
    }

    sed "$sed" -i $cronfile || error=$?
    info 'Done' $error
} #---------------------------------------------------------------------------------------------------------------------
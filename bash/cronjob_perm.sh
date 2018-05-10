#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    info 'Set job(s) to run everyday'; printf "\n"

    for id in "${jobs[@]}"; {
        sed="s|;.*$id.*$||g;/.*$id/ s| [0-9][0-9] [0-9][0-9] \*| \* \* \*|g;"$sed
        printf "$id\n"
    }

    sed "$sed" -i $cronfile || error=$?
    info 'Done' $error

} #---------------------------------------------------------------------------------------------------------------------
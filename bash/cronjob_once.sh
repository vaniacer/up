#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    # Get time
    date=${date% *}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}

    printf "\nSet job $job_id to run once\n"
    sed="s|^.*-C $job_id.*$|&; sed '/$job_id/d' -i '$cronfile'|g;/.*$job_id/ s|\* \* \*|$DD $MM \*|g"
    sed "$sed" -i $cronfile || error=$?

} #---------------------------------------------------------------------------------------------------------------------
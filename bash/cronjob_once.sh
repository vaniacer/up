#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    # Get time
    date=${date% *}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}

    printf "\nSet job(s) to run once:\n"

    for id in "${jobs[@]}"; {
        sed="s|^.*-C $id.*$|&; sed '/$id/d' -i '$cronfile'|g;/.*$id/ s|\* \* \*|$DD $MM \*|g;"$sed
        printf "$id\n"
    }

    sed "$sed" -i $cronfile || error=$?

} #---------------------------------------------------------------------------------------------------------------------
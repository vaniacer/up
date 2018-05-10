#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nMake permanent cron job(s):\n"; for i in "${jobs[@]//\'/}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    # Get time
    date=${date% *}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}

    info 'Make job(s) to run once'
    for id in "${jobs[@]}"; {
        sed="s|^.*-C $id.*$|&; sed '/$id/d' -i '$cronfile'|g;/.*$id/ s|\* \* \*|$DD $MM \*|g;"$sed
        printf "\n$id"
    }

    sed "$sed" -i $cronfile || error=$?
    info 'Done' $error

} #---------------------------------------------------------------------------------------------------------------------
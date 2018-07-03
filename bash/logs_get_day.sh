#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nGet current day logs from server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr              # Get server address
    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key

    arhive="$tmp_folder/${addr}_daylogs_`printf "%(%d-%m-%Y)T"`.zip"

    ssh -t -t $sopt $addr "
        find $wdir/jboss-bas-*/standalone/log -type f -daystart -ctime 0 | xargs zip -jy $arhive > /dev/null" && {

            echo -e "\nСоздан архив \"$arhive\"."; download "$arhive"

        } || { error=$?; printf "No files found."; }

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nGet all logs from server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr              # Get server address
    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/temp/$key

    arhive="$tmp_folder/${addr}_allogs_`printf "%(%d-%m-%Y)T"`.zip"

    ssh -t -t $sopt $addr "zip -jy $arhive $wdir/jboss-bas-*/standalone/log/* > /dev/null" && {

        echo -e "\nСоздан архив \"$arhive\"."; download "$arhive"

    } || error=$?

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
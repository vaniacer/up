#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nGet all logs from server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key

    arhive="$tmp_folder/allogs.zip"

    ssh $sopt $addr "zip -jy $arhive $wdir/jboss-bas-*/standalone/log/* > /dev/null" && {

        echo -e "\nСоздан архив \"$arhive\"."; download

    } || error=$?

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
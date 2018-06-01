#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nGet current day logs from server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key

    arhive="$tmp_folder/daylogs.zip"

    ssh -ttt $sopt $addr "
        find $wdir/jboss-bas-*/standalone/log -type f -daystart -ctime 0 | xargs zip -jy $arhive > /dev/null" && {

            echo -e "\nСоздан архив \"$arhive\"."; download

        } || { error=$?; printf "No files found."; }

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
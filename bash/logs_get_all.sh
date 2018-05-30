#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nGet all logs from server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key

    arhive="$tmp_folder/allogs.zip"

    ssh $sopt $addr "zip -jy $arhive $wdir/jboss-bas-*/standalone/log/* > /dev/null" && {

        echo -e "\nСоздан архив \"$arhive\"."; download
        ssh $sopt $addr "rm $arhive" || error=$?

    } || error=$?

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
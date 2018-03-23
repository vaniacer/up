#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nGet DB dump from server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    arhive="$wdir/updates/allogs.zip"

    printf "\n"
    ssh $sopt $addr "zip -jy $arhive $wdir/jboss-bas-*/standalone/log/* > /dev/null" && {

        echo -e "\nСоздан архив \"$arhive\"."; download
        ssh $sopt $addr "rm $arhive" || error=$?

    } || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nGet DB dump from server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    printf "\n"
    arhive="$wdir/updates/daylogs.zip"
    ssh $sopt $addr "
        find $wdir/jboss-bas-*/standalone/log -type f -daystart -ctime 0 | xargs zip -jy $arhive > /dev/null" && {

            echo -e "\nСоздан архив \"$arhive\"."; download
            ssh $sopt $addr "rm $arhive" || error=$?

        } || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
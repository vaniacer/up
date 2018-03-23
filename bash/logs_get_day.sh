#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nGet DB dump from server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    printf "\n"
    ssh $sopt $addr "
        find    $wdir/jboss-bas-*/standalone/log -type f -daystart -ctime 0 | xargs \
        zip -jy $wdir/updates/daylogs.zip '{}'> /dev/null
        " && {
            echo -e "\nСоздан архив \"$wdir/updates/daylogs.zip\"."; download
            ssh $sopt $addr "rm $wdir/updates/daylogs.zip" || error=$?
        } || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
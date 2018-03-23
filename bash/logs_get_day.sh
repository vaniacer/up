#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nGet DB dump from server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    printf "\n"
    mydate=`date +'%Y-%m-%d'`
    ssh $sopt $addr "
        zip -jy $wdir/updates/daylogs.zip $wdir/jboss-bas-*/standalone/log/{*$mydate*,server.log} > /dev/null" && {

        echo -e "\nСоздан архив \"$wdir/updates/daylogs.zip\"."; download
        ssh $sopt $addr "rm $wdir/updates/daylogs.zip" || error=$?

    } || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
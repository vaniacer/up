#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Get DB dump from server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $sopt $addr "zip -jy $wdir/updates/allogs.zip $wdir/jboss-bas-*/standalone/log/* > /dev/null" && {

        echo -e "Создан архив \"$wdir/updates/allogs.zip\"."; download
        ssh $sopt $addr "rm $wdir/updates/allogs.zip" || error=$?

    } || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
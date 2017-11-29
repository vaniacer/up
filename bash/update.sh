#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Update server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
    printf   "with update(s):\n"; for i in "${updates[@]}"; { echo "$i"; }
}

function restore () { # Run system restore if jboss-start ended with errors.

    [[ "$error" = 0 ]] && return

    echo -e   "\n<b>Update ended with errors. Restore system files from - $bkp.</b>"
    ssh $sopt $addr "$wdir/krupd restore sys $bkp" || error=$?

    echo -e "\n<b>Start jboss.</b>\n"
    ssh $sopt $addr $wdir/krupd jboss.start || error=$?
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    echo -e "<b>Backup.</b>"
    ssh $sopt $addr $wdir/krupd bkp db  || error=$?; download
    ssh $sopt $addr $wdir/krupd bkp sys || error=$?; download; bkp=$name

    echo -e "<b>Copy update - ${updates##*/}.</b>\n"
    rsync -e"ssh $sopt" --progress -lzuogthvr $updates $addr:$wdir/updates/new/ || error=$?

    echo -e "<b>Start dummy page.</b>\n"
    ssh $sopt $addr '~/.utils/dp.sh --start' || error=$?

    echo -e "<b>Stop jboss.</b>"
    ssh $sopt $addr $wdir/krupd jboss.stop   || error=$?

    echo -e "\n<b>Update files.</b>"
    ssh $sopt $addr "unzip -o $wdir/updates/new/${updates##*/} \
        -d $wdir/jboss-bas-*/standalone/deployments" || error=$?

    echo -e "\n<b>Start jboss.</b>"
    ssh $sopt $addr $wdir/krupd jboss.start || error=$?; restore

    echo -e "<b>Stop dummy page.</b>"
    ssh $sopt $addr '~/.utils/dp.sh --stop' || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
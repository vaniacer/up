#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nUpdate server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
    printf   "\nwith update(s):\n"; for i in "${updates[@]}"; { echo "${i##*/}"; }
}

function restore () { # Run system restore if jboss-start ended with errors.

    [[ "$error" = 0 ]] && return

    echo -e   "\n<b>Update ended with errors. Restore system files from - $bkp.</b>"
    ssh $sopt $addr "$wdir/krupd restore sys $bkp" || error=$?

    echo -e "\n<b>Start jboss.</b>\n"
    ssh $sopt $addr $wdir/krupd jboss.start || error=$?
}

function body-test () { #--------------------------------| Main function |---------------------------------------------------

    #echo -e "<b>Backup.</b>"
    #ssh $sopt $addr $wdir/krupd bkp db  || error=$?; download
    #ssh $sopt $addr $wdir/krupd bkp sys || error=$?; download; bkp=$name

    filename=${updates##*/}

    echo -e "\n<b>Copy update - $filename.</b>\n"
    rsync -e"ssh $sopt" --progress -lzuogthvr $updates $addr:$wdir/updates/new/ && {

        echo -e "<b>Start dummy page.</b>\n"
        ssh $sopt $addr '~/.utils/dp.sh --start' || error=$?

        echo -e "<b>Stop jboss.</b>"
        ssh $sopt $addr $wdir/krupd jboss.stop   || error=$?

        echo -e "\n<b>Unzip files.</b>"
        ssh $sopt $addr "unzip -o $wdir/updates/new/$filename \
            -d $wdir/updates/update > /dev/null" || error=$?

        echo -e "\n<b>Copy files.</b>"
        ssh $sopt $addr "cp $wdir/updates/update/updates/deployments/*.{ear,jar,war} \
            $wdir/jboss-bas-*/standalone/deployments" || error=$?
        ssh $sopt $addr "cp $wdir/updates/update/updates/templates/* $wdir/templates" || error=$?
        ssh $sopt $addr "rm $wdir/expimp/*;  cp $wdir/updates/update/updates/expimp/* $wdir/expimp" || error=$?
        ssh $sopt $addr "cp $wdir/updates/update/updates/system_params.list.txt $wdir" || error=$?

        echo -e "\n<b>Start jboss.</b>"
        ssh $sopt $addr $wdir/krupd jboss.start || error=$?

        echo -e "\n<b>Export\Import.</b>"
        ssh $sopt $addr "cd $wdir; ./DataCreatorUpdate.sh; ./import_ByUUID_Central.sh" || error=$?

        echo -e "<b>Stop dummy page.</b>"
        ssh $sopt $addr '~/.utils/dp.sh --stop' || error=$?

    } || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function body () {

    printf "\nUnder construction.\n"

}

function run () {

    [[ ${#updates[*]} -gt 1 ]] && { printf "\nMultiple dumps selected, need one.\n"; error=1; } || {

        for server in "${servers[@]}"; { addr; body; }; info 'Done' $error

    }
}
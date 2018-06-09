#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nBackup full on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr              # Get server address
    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key

    # Copy dbdump script to server
    rsync -e "ssh $sopt" --progress -lzuogthvr $workdir/remote_{db,sys}.sh $addr:$tmp_folder > /dev/null || error=$?

    # DB backup and download
    ssh -ttt $sopt $addr "cd $tmp_folder; bash remote_db.sh $wdir" \
        && download "$tmp_folder/"*.gz || error=$?

    # System backup and download
    ssh -ttt $sopt $addr "cd $tmp_folder; bash remote_sys.sh $wdir" \
        && download "$tmp_folder/"*.zip || error=$?

    # Move files to backup folder
    ssh -ttt $sopt $addr "mv $tmp_folder/*.{gz,zip} $wdir/backup" || error=$?

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
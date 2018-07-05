#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nBackup full on server:\n$addr"
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    addr              # Get server address
    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/temp/$key

    # Copy dbdump script to server
    rsync -e "ssh $sopt" --progress -lzuogthvr $workdir/remote_{db,sys}.sh $addr:$tmp_folder > /dev/null || error=$?

    # DB backup and download
    filename1=`ssh $sopt $addr "cd $tmp_folder; bash remote_db.sh $wdir ${addr}_dbdump"` \
        && download "$tmp_folder/$filename1" || error=$?

    # System backup and download
    filename2=`ssh $sopt $addr "cd $tmp_folder; bash remote_sys.sh $wdir ${addr}_system"` \
        && download "$tmp_folder/$filename2" || error=$?

    # Move files to backup folder
    ssh $sopt $addr "mv $tmp_folder/{$filename1,$filename2} $wdir/backup" || error=$?

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
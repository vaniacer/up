#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nBackup database on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr              # Get server address
    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key

    # Copy dbdump script to server
    rsync -e "ssh $sopt" --progress -lzuogthvr $workdir/remote_db.sh $addr:$tmp_folder > /dev/null || error=$?

    # Run script, run download
    filename=`ssh -ttt $sopt $addr "cd $tmp_folder; bash remote_db.sh $wdir ${addr}_dbdump"` \
        && download "$tmp_folder/$filename" || error=$?

    # Move dump to backup folder
    ssh -ttt $sopt $addr "mv $tmp_folder/$filename $wdir/backup" || error=$?

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
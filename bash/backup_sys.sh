#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nBackup system on server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr              # Get server address
    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/temp/$key

    # Copy archive maker to server
    rsync -e "ssh $sopt" --progress -lzuogthvr $workdir/remote_sys.sh $addr:$tmp_folder > /dev/null || error=$?

    # Run script, run download
    filename=`ssh -t -t $sopt $addr "cd $tmp_folder; bash remote_sys.sh $wdir ${addr}_system"` \
        && download "$tmp_folder/$filename" || error=$?

    # Move archive to backup folder
    ssh $sopt $addr "mv $tmp_folder/$filename $wdir/backup" || error=$?

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
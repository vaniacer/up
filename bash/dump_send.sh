#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nCopy DB dump $updates to server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    [[ ${#dumps[*]} -gt 1 ]] && { printf "\nMultiple dumps selected, need one.\n"; error=1; return 1; }

    addr              # Get server address
    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key
    
    filename=$dumps
    warning "You are sending dump - <b>$filename</b>\nto server - <b>$addr</b>\n\n" 30

    printf "\nCopy dump.\n"
    rsync -e "ssh $sopt" --progress -lzuogthvr "$dumpdir/$pname/$dumps" $addr:$tmp_folder && {

        ssh $sopt $addr "cd $wdir; ./krupd restore db $tmp_folder/$filename" || error=$?

    } || error=$?

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
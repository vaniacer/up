#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nCopy DB dump $dbdumps to server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    [[ ${#dbdumps[*]} -gt 1 ]] && { printf "\nMultiple dumps selected, need one.\n"; error=1; return 1; }

    addr              # Get server address
    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/temp/$key
    
    warning "You are sending dump - <b>$dbdumps</b>\nto server - <b>$addr</b>\n\n" 30

    printf "\nCopy dump.\n"
    rsync -e "ssh $sopt" --progress -lzuogthvr "$dumpdir/$pname/$dbdumps" $addr:$tmp_folder && {

        ssh -t -t $sopt $addr "cd $wdir; ./krupd restore db $tmp_folder/$dbdumps" || error=$?

    } || error=$?

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
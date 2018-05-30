#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nRun SQL script(s):\n"; for i in "${scripts[@]//\'/}"; { echo "${i##*/}"; }
    printf      "\non Server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    create_tmp_folder # Creates tmp folder tmp_folder=$tmp_folder/$key

    for file in "${scripts[@]}"; { filename=${file##*/}

        # Copy script to server
        rsync -e "ssh $sopt" --progress -lzuogthvr $file $addr:$tmp_folder/ > /dev/null && {

            # Run script
            result=`ssh $sopt $addr "$wdir/krupd execsql $tmp_folder/$filename"` || error=$?

            # Show result
            printf "$result\n"

            # Save result to make it downloadable
            cat >> $dumpdir/${filename}_$key.log <<< "$result"

        } || error=$?
    }

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

    printf "\n<b>Log file will be stored until tomorrow, please download it if you need this file!</b>"
    printf "\n<a class='btn btn-primary' href='/dumps/${filename}_$key.log'>Download</a>\n"

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nRun SQL script(s):\n"; for i in "${scripts[@]}"; { echo "${i##*/}"; }
    printf      "\non Server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    printf "\n"
    for file in "${scripts[@]}"; { filename=${file##*/}

        # Copy script to server
        rsync -e "ssh $sopt" --progress -lzuogthvr $file $addr:$wdir/updates/new/ > /dev/null && {

            # Run script
            result=`ssh $sopt $addr "$wdir/krupd execsql $wdir/updates/new/$filename"` || error=$?

            # Show result
            printf "$result\n"

            # Save result to make it downloadable
            cat >> $dumpdir/${filename}_$key.log <<< "$result"

            # Delete script after execution
            ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?

        } || error=$?
    }
    printf "\n<b>Log file will be stored until tomorrow, please download it if you need this file!</b>"
    printf "\n<a class='btn btn-primary' href='/dumps/${filename}_$key.log'>Download</a>\n"
} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
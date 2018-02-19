#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nRun SQL script(s):\n"; for i in "${scripts[@]}"; { echo "${i##*/}"; }
    printf      "\non Server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    for file in "${scripts[@]}"; { filename=${file##*/}

        # Copy script to server
        rsync -e "ssh $sopt" --progress -lzuogthvr $file $addr:$wdir/updates/new/ > /dev/null && {

            # Run script
            result=`ssh $sopt $addr "$wdir/krupd execsql $wdir/updates/new/$filename"` || error=$?

            # Show result
            printf "$result\n"

            # Save result to make it downloadable
            [[ -d $dumpdir/$pname ]] || mkdir $dumpdir/$pname
            cat >> $dumpdir/$pname/sql_$key.txt <<< "$result"

            # Delete script after execution
            ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?

        } || error=$?
    }
    printf "\n\n<a class='btn btn-primary' href='/download_dump/$prj/sql_$key.txt'>Download</a>\n"
} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
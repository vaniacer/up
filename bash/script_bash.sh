#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nRun BASH script(s):\n"; for i in "${scripts[@]}"; { echo "${i##*/}"; }
    printf       "\non Server(s):\n"; for i in "${servers[@]}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    check_updates_folder

    for file in "${scripts[@]}"; { filename=${file##*/}

        printf "\n"
        # If updates where selected copy them too and add as options to the script
        [[ ${updates[@]} ]] && {
            rsync -e "ssh $sopt" --progress -lzuogthvr ${updates[@]} $addr:$wdir/updates/new && {
                for U in ${updates[@]}; { opt+=" updates/new/${U##*/}"  ; }
            } || { error=$?; echo -e "\nFile copy error."; return $error; }
        }

        # Copy script to server
        rsync -e "ssh $sopt" --progress -lzuogthvr $file $addr:$wdir/updates/new/ > /dev/null && {

            printf "\nRun  script - $filename\n"
            ssh $sopt $addr "cd $wdir; chmod +x updates/new/$filename; updates/new/$filename $opt" || {
                error=$?; printf "\nScript ended with error: $error\n"
            }

            # Delete script after execution
            ssh $sopt $addr "rm $wdir/updates/new/$filename" || error=$?

        } || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
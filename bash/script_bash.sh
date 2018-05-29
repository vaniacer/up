#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nRun BASH script(s):\n"; for i in "${scripts[@]//\'/}"; { echo "${i##*/}"; }
    printf       "\non Server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key

    for file in "${scripts[@]}"; { filename=${file##*/}

        # If updates where selected copy them too and add as options to the script
        [[ ${updates[@]} ]] && {
            rsync -e "ssh $sopt" --progress -lzuogthvr ${updates[@]} $addr:$tmp_folder && {
                for U in ${updates[@]}; { opt+=" $tmp_folder/${U##*/}"  ; }
            } || { error=$?; echo -e "\nFile copy error."; return $error; }
        }

        # Copy script to server
        rsync -e "ssh $sopt" --progress -lzuogthvr $file $addr:$tmp_folder > /dev/null && {

            printf "Run  script - $filename\n"
            ssh $sopt $addr "cd $wdir; bash $tmp_folder/$filename $opt" || {
                error=$?; printf "\n<b>Script ended with error: $error</b>\n"
            }

            # Delete tmp folder after execution
            ssh $sopt $addr "rm -r $tmp_folder" || error=$?

        } || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
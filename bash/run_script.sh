#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nRun script(s):\n"; for i in "${scripts[@]//\'/}"; { echo "${i##*/}"; }
    printf     "\non Server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key

    # If updates where selected copy them too and add as options to the script
    [[ ${updates[@]} ]] && {
        rsync -e "ssh $sopt" --progress -lzuogthvr ${updates[@]} $addr:$tmp_folder && {
            for U in ${updates[@]}; { opt+=" $tmp_folder/${U##*/}"  ; }
        } || { error=$?; echo -e "\nscript copy error."; return $error; }
    }

    for script in "${scripts[@]}"; { filename=${script##*/}; type=${filename##*.}

        printf "\n<b>Run script - $filename</b>\n"

        case $type in
            yml)
                [[ $sopt ]] && extra="--ssh-extra-args=$sopt"

                printf "\n$script\n"
                ansible-playbook $script -i "$addr," $extra --vault-password-file ~/vault.txt --syntax-check \
                    || error=$?

                ansible-playbook $script -i "$addr," $extra --vault-password-file ~/vault.txt || error=$?
                continue;;
        esac

        # Copy script to server
        rsync -e "ssh $sopt" --progress -lzuogthvr $script $addr:$tmp_folder > /dev/null && {

            case $type in

                sh)
                    ssh $sopt $addr "cd $wdir; bash $tmp_folder/$filename $opt" || {
                    error=$?; printf "\n<b>Script ended with error: $error</b>\n"
                };;

                py)
                    ssh $sopt $addr "cd $wdir; python $tmp_folder/$filename $opt" || {
                    error=$?; printf "\n<b>Script ended with error: $error</b>\n"
                };;

                sql)
                    # Run script
                    result=`ssh $sopt $addr "$wdir/krupd execsql $tmp_folder/$filename"` || error=$?

                    # Show result
                    printf "$result\n"

                    # Save result to make it downloadable
                    cat >> $dumpdir/${filename}_$key.log <<< "$result"

                    printf "\n<b>Log script will be stored until tomorrow, please download it if you need this script!</b>"
                    printf "\n<a class='btn btn-primary' href='/dumps/${filename}_$key.log'>Download</a>\n";;
            esac

        } || error=$?
    }

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
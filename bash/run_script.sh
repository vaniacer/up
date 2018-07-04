#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nRun script(s):\n"; for i in "${scripts[@]//\'/}"; { echo "${i##*/}"; }
    printf     "\non Server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr              # Get server address
    create_tmp_folder # Creates tmp folder tmp_folder=$wdir/updates/new/$key

    # If updates where selected copy them too and add as options to the script
    [[ ${updates[@]} ]] && {
        rsync -e "ssh $sopt" --progress -lzuogthvr ${updates[@]} $addr:$wdir/updates/new/ && {
            for U in ${updates[@]}; { file_opt+=" $wdir/updates/new/${U##*/}"  ; }
        } || { error=$?; echo -e "\nscript copy error."; return $error; }
    }

    for ((i=0; i<${#scripts[@]}; i++)); {

        filename="${scripts[$i]##*/}"
        scrptype="${filename##*.}"
        soptions="${scropts[$i]}"

        printf "\n<b>Run script - $filename</b>\n"

        case $scrptype in
            yml)
                ansible-playbook ${scripts[$i]} -i "$addr," --vault-password-file ~/vault.txt --syntax-check \
                    || { error=$?; continue; }
                ansible-playbook ${scripts[$i]} -i "$addr," --vault-password-file ~/vault.txt || error=$?
                continue;;
        esac

        # Copy script to server
        rsync -e "ssh $sopt" --progress -lzuogthr ${scripts[$i]} $addr:$tmp_folder > /dev/null && {

            case $scrptype in

                sh)
                    ssh -t -t $sopt $addr "cd $wdir; bash $tmp_folder/$filename $soptions $file_opt"   || {
                    error=$?; printf "\n<b>Script ended with error: $error</b>\n"
                };;

                py)
                    ssh -t -t $sopt $addr "cd $wdir; python $tmp_folder/$filename $soptions $file_opt" || {
                    error=$?; printf "\n<b>Script ended with error: $error</b>\n"
                };;

                sql)
                    # Copy sqlaunch script to server
                    rsync -e "ssh $sopt" --progress -lzuogthr $workdir/remote_sql.sh $addr:$tmp_folder > /dev/null \
                        || error=$?

                    # Run script
                    result=`ssh -t -t $sopt $addr "cd $tmp_folder; bash remote_sql.sh $wdir $filename"` && {

                        # Show result
                        printf "\n$result\n"

                        # Save result to file and make it downloadable
                        cat >> $dumpdir/${filename}_$key.log <<< "$result"

                        printf "\n<b>Log will be stored until tomorrow, download it please if you need it!</b>"
                        printf "\n<a class='btn btn-primary' href='/dumps/${filename}_$key.log'>Download</a>\n"

                    } || { error=$?; printf "\n$result\n"; };;

                *)
                    printf "Unknown script type, exit.\n"
                    error=1; continue;;

            esac

        } || error=$?
    }

    # Delete tmp folder after execution
    ssh $sopt $addr "rm -r $tmp_folder" || error=$?

} #---------------------------------------------------------------------------------------------------------------------
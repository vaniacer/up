#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Update server(s):\n${servers// /\\n}\n\nwith update(s):\n${updates// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { #ssh ${addr} "${wdir}/krupd bkp full" || error 'Backup'

                 for file in ${updates}; {
                    filename=$(basename ${file})
                    echo -e "\nCopy file - ${filename}"

                    # Check if file exist, copy if not exist
                    ssh ${addr} ls ${wdir}/updates/new/${filename} &> /dev/null \
                        && { echo -e "File - ${filename} exist, skip."; } \
                        || { scp ${file} ${server}/updates/new || error=$?; }
                 }
                 # Update
                 ssh ${addr} '~/.utils/dp.sh --start && echo -e \\nStart dummy page.\\n' || error 'Dummy page'
                 ssh ${addr} ${wdir}/krupd jboss.stop  || error 'Jboss stop'

                 echo -e "\n<b>Update files.</b>\n"

                 ssh ${addr} ${wdir}/krupd jboss.start || error 'Jboss start'
                 ssh ${addr} '~/.utils/dp.sh --stop && echo -e \\nStop dummy page.\\n' || error 'Dummy page'; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
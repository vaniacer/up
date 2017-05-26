#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Update server(s):\n${servers// /\\n}\n\nwith update(s):\n${updates// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && {                                                                      echo -e "\n<b>Backup.</b>"
                 . ${workdir}/backup_full.sh    ; run 'silent' || error 'Backup'    ; echo -e "\n<b>Copy update.</b>"
                 . ${workdir}/copy.sh           ; run 'silent' || error 'Copy'      ; echo -e "<b>"
                 . ${workdir}/maintenance_on.sh ; run 'silent' || error 'Dummy page'; echo -e "\nStop jboss.</b>\n"
                 . ${workdir}/stop.sh           ; run 'silent' || error 'Jboss stop'; echo -e "\n<b>Update files.</b>\n"

                 ssh ${addr} "
                    unzip -o ${wdir}/updates/new/${filename} \
                    -d jboss-bas-*/standalone/deployments"     || error=$?; echo -e "\n<b>Start jboss.</b>\n"

                 . ${workdir}/start.sh          ; run 'silent' || error 'Jboss start'; echo "<b>"
                 . ${workdir}/maintenance_off.sh; run 'silent' || error 'Dummy page' ; echo "</b>"; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
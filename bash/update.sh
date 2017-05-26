#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Update server(s):\n${servers// /\\n}\n\nwith update(s):\n${updates// /\\n}\n"; exit 0
}

 # Run system restore if there where error on jboss start.
function restore () { [ ${error} -gt 0 ] && {
    echo -e "\n<b>Restore system files - ${bkp}.</b>"
    ssh ${addr} "${wdir}/krupd restore sys ${bkp}" || error=$?

    echo -e "\n<b>Start jboss.</b>\n"
    . ${workdir}/start.sh; run 0 || error 'Jboss start'
}; }

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && {                                                                      echo -e "\n<b>Backup.</b>"
                . ${workdir}/backup_full.sh   ; run 0 || error 'Backup'; bkp=${name}; echo -e "<b>Copy update.</b>"
                . ${workdir}/copy.sh          ; run 0 || error 'Copy'               ; echo -e "<b>"
                . ${workdir}/maintenance_on.sh; run 0 || error 'Dummy page'         ; echo -e "\nStop jboss.</b>\n"
                . ${workdir}/stop.sh          ; run 0 || error 'Jboss stop'         ; echo -e "\n<b>Update files.</b>\n"

                ssh ${addr} "unzip -o ${wdir}/updates/new/${filename} \
                    -d jboss-bas-*/standalone/deployments"     || error=$?; echo -e "\n<b>Start jboss.</b>\n"

                . ${workdir}/start.sh          ; run 0 || error 'Jboss start'; restore; echo "<b>"
                . ${workdir}/maintenance_off.sh; run 0 || error 'Dummy page' ; echo "</b>"; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
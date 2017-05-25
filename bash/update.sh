#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Update server(s):\n${servers// /\\n}\n\nwith update(s):\n${updates// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    for server in ${servers}; { addr

        # Check access and run command or send 'Server unreachable'
        ssh ${addr} "echo > /dev/null" \
            && { #. ${workdir}/backup_full.sh   ; run 'silent' || error 'Backup'    ; echo

                 . ${workdir}/copy.sh           ; run 'silent' || error 'Copy'      ; echo

                 # Update
                 . ${workdir}/maintenance_on.sh ; run 'silent' || error 'Dummy page'; echo
                 . ${workdir}/stop.sh           ; run 'silent' || error 'Jboss stop'; echo

                 echo -e "<b>Update files.</b>\n"

                 . ${workdir}/start.sh          ; run 'silent' || error 'Jboss start'; echo
                 . ${workdir}/maintenance_off.sh; run 'silent' || error 'Dummy page' ; echo; } \
            || { error=$?; echo -e "\nServer unreachable."; }

    }; info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
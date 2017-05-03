#!/bin/bash

function description () {
    echo -e "Set cron job ${cmd} for server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    # Get time
    time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

    sedr="/${id}/d"                                         # Sed rule to delete old cron job
    date="${mm} ${hh} ${DD} ${MM}"                          # Cron format date
    cncl="sed \"${sedr}\" -i ${cronfile}\n"                 # Command to cancel executed cron job
    cmnd="${workdir}/starter.sh -cmd ${cmd} -cron ${id}"    # Command to run
    [ "${updates}" ] && cmnd="${cmnd} -u \"${updates}\""    # Add updates to command if exist
    [ "${servers}" ] && cmnd="${cmnd} -s \"${servers}\""    # Add servers to command if exist

    # Set crontab job
    echo -e "$(crontab -l)\n${date} * ${cmnd}; ${cncl}" | crontab -

    # Info
    ${workdir}/starter.sh -cmd "${cmd}" -u "${updates}" -s "${servers}" -desc true

    echo -e "\nDone.\nError: ${error}"
} #---------------------------------------------------------------------------------------------------------------------
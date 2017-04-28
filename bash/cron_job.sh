#!/bin/bash

# Get options and functions
. $(dirname $0)/func.sh
cronfile=/var/spool/cron/crontabs/${USER}

# Get time
time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

sedr="/${id}/d"                                         # Sed rule to delete old cron job
date="${mm} ${hh} ${DD} ${MM}"                          # Cron format date
cmnd="${workdir}/${cmd} -cron ${id}"                    # Command to run
cncl="sed \"${sedr}\" -i ${cronfile}"                   # Command to cancel executed cron job
[ "${updates}" ] && cmnd="${cmnd} -u \"${updates}\""    # Add updates to command if exist
[ "${servers}" ] && cmnd="${cmnd} -s \"${servers}\""    # Add servers to command if exist

# Set crontab job
echo -e "${date} * ${cmnd}; ${cncl}" >> ${cronfile}

# Info
${workdir}/${cmd} -u "${updates}" -s "${servers}" -desc true
#!/bin/bash

# Get options and functions
. $(dirname $0)/func.sh

# Get time
read date time <<< "${date}"
hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

date="${mm} ${hh} ${DD} ${MM}"                              # Cron format date
sedr="/${id}/d"                                             # Sed rule to delete old cron job
cncl="sed \"${sedr}\" -i /var/spool/cron/crontabs/${USER}"  # Command to cancel executed cron job
cmnd="${workdir}/${cmd} -cron ${id}"                         # Command to run
[ "${updates}" ] && cmnd="${cmnd} -u \"${updates}\""        # Add updates to command if exist
[ "${servers}" ] && cmnd="${cmnd} -s \"${servers}\""        # Add servers to command if exist

# Set crontab job
(crontab -l ; echo -e "${date} * ${cmnd}; ${cncl}") | crontab -

# Info
${workdir}/${cmd} -u "${updates}" -s "${servers}" -desc true
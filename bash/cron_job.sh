#!/bin/bash

# Get options and functions
error=0
workdir=$(dirname $0)
crondir=${workdir}/../../logs/cron
rundir=${workdir}/../../logs/run
#----------|Get opts|------------
until [ -z "$1" ]; do case $1 in

    -server | -s) servers=${2};;
    -update | -u) updates=${2};;
    -date   | -d) date=${2};;
    -cron   | -C) cron=${2};;
    -desc   | -D) desc=${2};;
    -job    | -j) jobs=${2};;
    -cmd    | -c) cmd=${2};;
    -key    | -k) key=${2};;
    -id     | -i) id=${2};;

esac; shift 2; done
#--------------------------------

# Get time
time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

sedr="/${id}/d"                                         # Sed rule to delete old cron job
date="${mm} ${hh} ${DD} ${MM}"                          # Cron format date
cncl="sed \"${sedr}\" -i ${cronfile}\n"                 # Command to cancel executed cron job
cmnd="${workdir}/starter.sh -cmd ${cmd} -cron ${id}"    # Command to run
[ "${updates}" ] && cmnd="${cmnd} -u \"${updates}\""    # Add updates to command if exist
[ "${servers}" ] && cmnd="${cmnd} -s \"${servers}\""    # Add servers to command if exist

# Set crontab job
$(crontab -l; echo -e "\n${date} * ${cmnd}; ${cncl}") | crontab -

# Info
${workdir}/starter.sh -cmd "${cmd}" -u "${updates}" -s "${servers}" -desc true
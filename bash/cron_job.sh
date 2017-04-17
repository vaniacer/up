#!/bin/bash

folder=$(dirname $0)

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) servers=${2};;
	    -update | -u) updates=${2};;
	    -date   | -d) date=${2};;
	    -cmd    | -c) cmd=${2};;
	             -id) id=${2};;
    esac

    shift 2
done

# Get time
read date time <<< "${date}"
hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

date="${mm} ${hh} ${DD} ${MM}"                              # Cron format date
sedr="/${id}/d"                                             # Sed rule to delete old cron job
cncl="sed \"${sedr}\" -i /var/spool/cron/crontabs/${USER}"  # Command to cancel executed cron job
cmnd="${folder}/${cmd}.sh -cron ${id}"                      # Command to run
[ "${updates}" ] && cmnd="${cmnd} -u \"${updates}\""        # Add updates to command if exist
[ "${servers}" ] && cmnd="${cmnd} -s \"${servers}\""        # Add servers to command if exist

# Set crontab job
(crontab -l ; echo -e "${date} * ${cmnd}; ${cncl}") | crontab -

# Info
${folder}/${cmd}.sh -u "${updates}" -s "${servers}" -desc true
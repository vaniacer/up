#!/bin/bash

folder=$(dirname $0)
logdir=${folder}/../../logs/cron

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
mess="Set new cronjob. Run date: ${date} ${time}\n"
hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

date="${mm} ${hh} ${DD} ${MM}"                                                # Cron format date
sedr="/${id}/d"                                                               # Sed rule to delete old cron job
cmnd="${folder}/${cmd}.sh -u \"${updates}\" -s \"${servers}\" -cron ${id}"    # Command to run
cncl="(crontab -l | sed \"${sedr}\") | crontab -"                             # Command to cancel executed cron job

# Set crontab job
(crontab -l ; echo -e "${date} * ${cmnd} ; ${cncl}") | crontab -

# Info
echo -e "${mess}"
${folder}/${cmd}.sh -u "${updates}" -s "${servers}" -desc true
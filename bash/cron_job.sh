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
case ${date} in
    '__DATE__')
        DD=$(date +'%d')
        MM=$(date +'%m')
        hh=$(date +'%H')
        mm=$(date +'%M'); ((mm++))
        [ ${mm} -gt 59 ] && { mm=00; ((hh++)); [ ${hh} -gt 23 ] && hh=00; };;
    *:*)
        time=${date#* }; date=${date% *}
        hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*};;
esac

date="${mm} ${hh} ${DD} ${MM}"                                                # Cron format date
sedr="/${id}/d"                                                               # Sed rule to delete old cron job
cmnd="${folder}/${cmd}.sh -u \"${updates}\" -s \"${servers}\" -cron ${id}"    # Command to run
cncl="(crontab -l | sed \"${sedr}\") | crontab -"                             # Command to cancel executed cron job

# Set crontab job
(crontab -l ; echo -e "${date} * ${cmnd}; ${cncl}") | crontab -

# Info
echo -e "Setting cron job id: ${id}, date: ${DD}.${MM} ${hh}:${mm}\n"
${folder}/${cmd}.sh -u "${updates}" -s "${servers}" -desc true
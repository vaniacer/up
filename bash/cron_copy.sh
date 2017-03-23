#!/bin/bash

#set -e

folder=$(cd "$(dirname "$0")" && pwd)

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) servers=${2};;
	    -update | -u) updates=${2};;
	    -date   | -d) date=${2};;
	    -time   | -t) time=${2};;
    esac

    shift 2
done

# Full path for updates
for u in ${updates}; do updates_full+=("${folder}/../${u}"); done

# Get time
hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

date="${mm} ${hh} ${DD} ${MM}"                                          # Cron format date
sedr="/${date}/d"                                                       # Sed rule to delete old cron job
cmnd="${folder}/copy.sh -u \"${updates_full[@]}\" -s \"${servers[@]}\"" # Command to run
cncl="(crontab -l | sed \"${sedr}\") | crontab -"                       # Command to cancel executed cron job

# Check if job with the same time exist, time have to be unique
crontab -l | grep "${date}" > /dev/null && {
    echo -e "На это время запланировано другое задание, измените время!"
    exit 1
}

# Info
echo -e "Setting cron job for copy Updates:"
for u in ${updates_full[@]}; do echo ${u}; done
echo -e "\nTo Servers: \n"
for s in ${servers[@]}; do echo ${s}; done
echo

# Set crontab job
(crontab -l ; echo -e "${date} * ${cmnd}; ${cncl}") | crontab -
#!/bin/bash

#set -e

folder=$(dirname $0)

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) servers=${2};;
	    -update | -u) updates=${2};;
	    -date   | -d) date=${2};;
	    -time   | -t) time=${2};;
	             -id) id=${2};;
    esac

    shift 2
done

# Full path for updates
#for u in ${updates}; do updates_full+=("${folder}/../${u}"); done

# Get time
hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

# Cron format date
date="${mm} ${hh} ${DD} ${MM}"

# Sed rule to delete old cron job
sedr="/${id}/d"

# Command to run
cmnd="${folder}/copy.sh -u \"${updates[@]}\" -s \"${servers[@]}\""

# Command to cancel executed cron job
cncl="(crontab -l | sed \"${sedr}\") | crontab -"

# Check if job with the same time exist, time have to be unique
#crontab -l | grep "${date}" > /dev/null && {
#    echo -e "На это время запланировано другое задание, измените время!"
#    exit 1
#}

# Info
echo -e "Setting cron job for copy Updates:"
for u in ${updates[@]}; do echo ${u}; done
echo -e "\nto Servers:"
for s in ${servers[@]}; do echo ${s}; done
echo

# Set crontab job
(crontab -l ; echo -e "${date} * ${cmnd}; ${cncl}") | crontab -
#!/bin/bash

#set -e

folder=$(dirname $0)
logdir=${folder}/../../logs/cron

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

# Get time
case ${time} in
    '__TIME__')
        DD=$(date +'%d')
        MM=$(date +'%m')
        hh=$(date +'%H')
        mm=$(date +'%M'); ((mm++))
        [ ${mm} -gt 59 ] && { mm=00; ((hh++)); [ ${hh} -gt 23 ] && hh=00; };;
    *)
        hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*};;
esac

# Cron format date
date="${mm} ${hh} ${DD} ${MM}"

# Sed rule to delete old cron job
sedr="/${id}/d"

# Command to run
cmnd="${folder}/copy.sh -u \"${updates[@]}\" -s \"${servers[@]}\" -cron ${id}"

# Command to cancel executed cron job
cncl="(crontab -l | sed \"${sedr}\") | crontab -"

# Info
echo -e "Setting cron job for copy Updates:"
for u in ${updates[@]}; do echo ${u}; done
echo -e "\nto Servers:"
for s in ${servers[@]}; do echo ${s}; done
echo

# Set crontab job
(crontab -l ; echo -e "${date} * ${cmnd}; ${cncl}") | crontab -
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
case ${time}:${date} in
    '__TIME__':'__DATE__')
        DD=$(date +'%d')
        MM=$(date +'%m')
        hh=$(date +'%H')
        mm=$(date +'%M'); ((mm++))
        [ ${mm} -gt 59 ] && { mm=00; ((hh++)); [ ${hh} -gt 23 ] && hh=00; };;
    *:*)
        hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*};;
esac

date="${mm} ${hh} ${DD} ${MM}"                                                  # Cron format date
sedr="/${id}/d"                                                                 # Sed rule to delete old cron job
cmnd="${folder}/copy.sh -u \"${updates[@]}\" -s \"${servers[@]}\" -cron ${id}"  # Command to run
cncl="(crontab -l | sed \"${sedr}\") | crontab -"                               # Command to cancel executed cron job

# Set crontab job
(crontab -l ; echo -e "${date} * ${cmnd}; ${cncl}") | crontab -

# Info
echo -e "Setting cron job id: ${id}, date: ${DD}.${MM} ${hh}:${mm}\n"
echo -e "Copy Updates:"
for u in ${updates[@]}; do echo ${u}; done
echo -e "\nto Servers:"
for s in ${servers[@]}; do echo ${s}; done
echo
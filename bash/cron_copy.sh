#!/bin/bash

set -e

folder=$(cd "$(dirname "$0")" && pwd)

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -server | -s) server=true;  update=false; shift;;
	    -update | -u) update=true;  server=false; shift;;
	    -date   | -d) server=false; update=false; shift; date=$1;;
	    -time   | -t) server=false; update=false; shift; time=$1;;
    esac

    [ ${server} = true ] && servers+=($1)
    [ ${update} = true ] && updates+=(${folder}/../$1)

    shift
done

# Get time
hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

date="${mm} ${hh} ${DD} ${MM}"                              # Cron format date
sedr="/${date}/d"                                           # Sed rule to delete old cron job
cmnd="${folder}/copy.sh -u ${updates[@]} -s ${servers[@]}"  # Command to run
cncl="(crontab -l | sed \"${sedr}\") | crontab -"           # Command to cancel executed cron job

# Info
echo -e "Setting cron job."
echo -e "Servers: ${servers[@]}"
echo -e "Updates: ${updates[@]}"
echo

# Set crontab job
(crontab -l ; echo -e "${date} * ${cmnd}; ${cncl}") | crontab -
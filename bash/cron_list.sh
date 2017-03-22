#!/bin/bash

set -e

#Get opts
until [ -z "$1" ]; do

    case $1 in
	    -project | -p) project=$2; update=false; shift 2;;
    esac

done

crontab -l | grep ${project}
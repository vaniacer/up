#!/bin/bash

folder="$1"
arhive="${2:-system}_`printf "%(%d-%m-%Y)T"`.zip"

zip -ry $arhive \
    $folder/jboss-bas-*/standalone/configuration/* \
    $folder/jboss-bas-*/standalone/deployments/* \
    `find $folder -maxdepth 1 -type f` \
    $folder/templates > /dev/null

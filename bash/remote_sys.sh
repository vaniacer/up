#!/bin/bash

folder="$1"

filename="system_`printf "%(%d-%m-%Y)T"`.zip"

zip -ry $filename \
    $folder/jboss-bas-*/standalone/configuration/* \
    $folder/jboss-bas-*/standalone/deployments/* \
    `find $folder -maxdepth 1 -type f` \
    $folder/templates > /dev/null

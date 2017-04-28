#!/bin/bash

# Get options and functions
. $(dirname $0)/func.sh

function description () {
    echo -e "Update server(s):\n${servers// /\\n}\n\nwith update(s):\n${updates// /\\n}\n"; exit 0
}

function run () { #----------------------------------|Main function|----------------------------------------------------
    echo -e "Not ready yet"
    error=$?
    echo -e "\nDone.\nERROR: ${error}"
} #---------------------------------------------------------------------------------------------------------------------

starter # From func.sh
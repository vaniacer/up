#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Update server(s):\n${servers// /\\n}\n\nwith update(s):\n${updates// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------
    echo -e "Not ready yet"
    error=$?
    info 'Done' ${error}
} #---------------------------------------------------------------------------------------------------------------------
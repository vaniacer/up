#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nDelete selected dump(s):\n"; for i in "${dumps[@]}"; { echo "${i##*/}"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    description
    cd $dumpdir/$pname && rm ${dumps[@]} || error=$?

} #---------------------------------------------------------------------------------------------------------------------
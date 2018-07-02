#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    update=${updates[0]//\'/}
    update=${update##*/}
    addr > /dev/null
    printf "\nUpdate server:\n$addr"
    printf   "\nwith update:\n$update"
}

function body () {

    printf "\nUnder construction.\n"

}

function run () {

    [[ ${#updates[*]} -gt 1 ]] && { printf "\nMultiple files selected, need one.\n"; error=1; } || {

        addr; body; info 'Done' $error

    }
}
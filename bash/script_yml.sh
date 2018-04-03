#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nRun YAML playbook(s):\n"; for i in "${scripts[@]//\'/}"; { echo "${i##*/}"; }
    printf         "\non Server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    inv="${servers[*]//:*:*/,}"
    inv=${inv// /}

    printf "\n"
    for playbook in "${scripts[@]}"; {

        ansible-playbook $playbook -i $inv --vault-password-file ~/vault.txt --syntax-check || { error=$?; break; }
        ansible-playbook $playbook -i $inv --vault-password-file ~/vault.txt || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { info 'ansible-playbook'; body; info 'Done' $error; }
#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nRun YAML playbook(s):\n"; for i in "${scripts[@]//\'/}"; { echo "${i##*/}"; }
    printf         "\non Server(s):\n"; for i in "${servers[@]//\'/}"; { echo "${i%%:*}"; }
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    for server in "${servers[@]}"; { addr > /dev/null; }
    [[ $sopt ]] && extra="--ssh-extra-args=$sopt"

    for playbook in "${scripts[@]}"; {

        ansible-playbook $playbook -i "$addr", "$extra" --vault-password-file ~/vault.txt --syntax-check \
            || { error=$?; break; }

        ansible-playbook $playbook -i "$addr", "$extra" --vault-password-file ~/vault.txt || error=$?
    }

} #---------------------------------------------------------------------------------------------------------------------

function run () { info 'ansible-playbook'; body; info 'Done' $error; }
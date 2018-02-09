#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nGet DB dump from server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $sopt $addr "$wdir/krupd bkp db" || error=$?; download
    # функция download сохраняет имя файла дампа в переменной $name
    # удаляю файл $name на сервере после скачивания на ups
    [[ $name ]] && ssh $sopt $addr "rm $name"

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in "${servers[@]}"; { addr; body; }; info 'Done' $error; }
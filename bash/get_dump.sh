#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Get DB dump from server(s):\n${servers// /\\n}\n"; exit 0
}

function body () { #---------------------------------| Main function |--------------------------------------------------

    ssh $addr "$wdir/krupd bkp db" || error=$?; download
    # функция download сохраняет имя файла дампа в переменной $name
    # удаляю файл $name на сервере после скачивания на ups
    ssh $addr "rm $name" || error=$?

} #---------------------------------------------------------------------------------------------------------------------

function run () { for server in $servers; { addr; body; }; info 'Done' $error; }
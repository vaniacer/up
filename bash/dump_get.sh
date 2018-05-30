#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nGet DB dump from server:\n$addr"
}

function body () { #--------------------------------| Main function |---------------------------------------------------

    ssh $sopt $addr "$wdir/krupd bkp db" || error=$?; download "$pname"
    # функция download сохраняет имя файла дампа в переменной $name
    # удаляю файл $name на сервере после скачивания на ups
    [[ $name ]] && ssh $sopt $addr "rm $name"

} #---------------------------------------------------------------------------------------------------------------------

function run () { addr; body; info 'Done' $error; }
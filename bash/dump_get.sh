#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nGet DB dump from server:\n$addr"
}

function run () { #--------------------------------| Main function |---------------------------------------------------

    addr # Get server address
    ssh -ttt $sopt $addr "$wdir/krupd bkp db" || error=$?; download "$pname"
    # функция download сохраняет имя файла дампа в переменной $name
    # удаляю файл $name на сервере после скачивания на ups
    [[ $name ]] && ssh -ttt $sopt $addr "rm $name"

} #---------------------------------------------------------------------------------------------------------------------
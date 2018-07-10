#!/bin/bash

workdir=$(dirname $0)          # Work dir
rundir=$workdir/../../logs/run # Folder to store running tasks logs

for id in $@; {

    pid=`cat $rundir/pid$id`
    kill -2 $pid `ps -o pid= --ppid $pid`
    rm $rundir/*$id
}
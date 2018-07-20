#!/bin/bash

for id in $@; {
    OI=$IFS; IFS=$'\n'; pids=($(ps a | grep $id | grep -v grep)); IFS=$OI
    for pid in "${pids[@]}"; { pid=($pid); list+=" $pid"; }
    kill $list
}
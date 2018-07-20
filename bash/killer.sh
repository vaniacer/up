#!/bin/bash

IFS=$'\n'
for id in $@; {
    pids=($(ps a | grep $id | grep -v grep))
    for pid in "${pids[@]}"; { pid=($pid); list+=" $pid"; }
    kill $list
}
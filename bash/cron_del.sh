#!/bin/bash

set -e

commands=$1

echo -e "Отменяю задачи в кроне.\n"
echo ${commands}

eval "${commands}"


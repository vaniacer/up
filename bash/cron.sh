#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "Set cron job $run for server(s):\n"; for i in "${servers[@]}"; { echo "$i"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    # Get time
    time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

    date="$mm $hh $DD $MM *"                              # Cron format date
    opts=("${options[@]:6}")                              # Cut cron part from options
    cncl="sed \"/$key/d\" -i $cronfile\n"                 # Command to delete executed cron job
    cmnd="$workdir/starter.sh -c $run -C $key ${opts[@]}" # Command to run

    # Set crontab job
    echo -e "$(crontab -l)\n$date $cmnd; $cncl\n" | crontab - || error=$?

    # Info
    info 'Set cron job'
    $workdir/starter.sh -c "$run" "${opts[@]}" -desc true # Show description of running command
    info 'Done' $error

} #---------------------------------------------------------------------------------------------------------------------
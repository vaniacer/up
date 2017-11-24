#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    echo -e "Set cron job $run for server(s):\n${servers// /\\n}\n"; exit 0
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    # Get time
    time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date%%.*}; MM=${date#*.}; MM=${MM%.*}

    sedr="/$id/d"                                     # Sed rule to delete old cron job
    date="$mm $hh $DD $MM"                            # Cron format date
    cncl="sed \"$sedr\" -i $cronfile\n"               # Command to cancel executed cron job
    cmnd="$workdir/starter.sh -c $run -p $prj -C $id" # Command to run
    [[ "$updates" ]] && cmnd="$cmnd -u \"$updates\""  # Add updates to command if exist
    [[ "$scripts" ]] && cmnd="$cmnd -x \"$scripts\""  # Add scripts to command if exist
    [[ "$servers" ]] && cmnd="$cmnd -s \"$servers\""  # Add servers to command if exist

    # Set crontab job
    echo -e "$(crontab -l)\n$date * $cmnd; $cncl" | crontab - || error=$?

    # Info
    info 'Set cron job'
    ${workdir}/starter.sh -c "$run" -u "$updates" -x "$scripts" -s "$servers" -desc true
    info 'Done' $error

} #---------------------------------------------------------------------------------------------------------------------
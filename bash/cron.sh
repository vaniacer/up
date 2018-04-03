#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    printf "\nSet cron job $run for server(s):\n"; for i in "${servers[@]//\'/}"; { printf "${i%%:*}"; }
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    # Get time
    time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}

    date="$mm $hh $DD $MM *"                      # Cron format date
    cncl="sed '/$key/d' -i '$cronfile'\n"         # Command to delete executed cron job
    cmnd="$workdir/starter.sh -c $run -C $key"    # Command to run

    for ((i=0; i<${#options[*]}; i+=2)); do       # loop through options
        key_value=( ${options[@]:$i:2} )          # get key_value pairs
        case ${key_value[0]} in                   #
            -run|-cmd|-date|-hid|-cid) continue;; # Drop unnecessary options
        esac                                      #
        # assign  key__________________value pairs to cron command, wrap values with ''
        cmnd+=" ${key_value[0]} '${key_value[1]}'"
    done

    # Set crontab job
    # echo -e "$(crontab -l)\n$date $cmnd; $cncl\n" | crontab - || error=$?
    # printf "$date $cmnd; $cncl" >> "$cronfile" || error=$?
    JS="#`line '=' 28`| job $key start |`line '=' 28`"
    JE="#`line '=' 28`|  job $key end  |`line '=' 28`"
    printf "$JS\n$date $cmnd; $cncl$JE\n" >> "$cronfile" || error=$?

    # Info
    info 'Setting cron job'
    $cmnd -desc true # Show description of running command
    info 'Cron job is set' $error

} #---------------------------------------------------------------------------------------------------------------------
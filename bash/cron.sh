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

    for ((i=0; i<${#options[*]}; i+=2)); do       # Loop through options
        key_value=( ${options[@]:$i:2} )          # Get key_value pairs
        case ${key_value[0]} in                   #
            -run|-cmd|-date|-hid|-cid) continue;; # Drop unnecessary options
        esac                                      #
        # Assign  key__________________value pairs of options to command, wrap values with ''
        cmnd+=" ${key_value[0]} '${key_value[1]}'"
    done

    # Set crontab job
    JS="#`line '=' 28`| job $key start |`line '=' 28`"
    JE="#`line '=' 28`|  job $key end  |`line '=' 28`"
    printf "$JS\n$date $cmnd; $cncl$JE\n" >> "$cronfile" || error=$?

    # Info
    $cmnd -desc true || error=$? # Show description of running command

} #---------------------------------------------------------------------------------------------------------------------
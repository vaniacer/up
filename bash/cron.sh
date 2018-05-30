#!/bin/bash

function description () { #---------------------| Function description |------------------------------------------------
    addr > /dev/null
    printf "\nSet cron job $run for server:\n$addr"
}

function run () { #---------------------------------| Main function |---------------------------------------------------

    # Get time
    time=${date#* }; date=${date% *}; hh=${time%:*}; mm=${time#*:}; DD=${date##*-}; MM=${date#*-}; MM=${MM%-*}

    date="$mm $hh $DD $MM *"                   # Cron format date
    cncl="sed '/$key/d' -i '$cronfile'\n"      # Command to delete executed cron job
    cmnd="$workdir/starter.sh -c $run -C $key" # Command to run

    for (( i=0; i<${#options[*]}; i+=2 )); do  # Loop through options
              name=${options[$i]}              # Get option name
        case $name in                          # Check:
            -run|-cmd|-date|-hid|-cid)         #  drop
            continue;;                         #  unnecessary
        esac                                   #  options
        value="${options[($i+1)]}"             # Get option value
        # Assemble name & value pairs of options for cron and description
        optcrn+=" $name '$value'" # this string goes to crontab file, wrap values with ''
        optdsc+=( $name "$value") # this array used in description, values without ''
    done

    # Set crontab job
    JS="#`line '=' 28`| job $key start |`line '=' 28`"
    JE="#`line '=' 28`|  job $key end  |`line '=' 28`"
    printf "$JS\n$date $cmnd $optcrn; $cncl$JE\n" >> "$cronfile" || error=$?

    # Info
    $cmnd "${optdsc[@]}" -desc true || error=$? # Show description of command

} #---------------------------------------------------------------------------------------------------------------------
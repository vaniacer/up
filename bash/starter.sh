#!/bin/bash

error=0                                 # Error
width=120                               # Terminal width
options=("$@")                          # Save all options in an array, needed for cron
workdir=$(dirname $0)                   # Work dir
cronfile=/var/spool/cron/crontabs/$USER # UpS user's crontab file
dumpdir=$workdir/../media/dumps         # Folder to store dumps
crondir=$workdir/../../logs/cron        # Folder to store cronjob logs
rundir=$workdir/../../logs/run          # Folder to store running tasks logs
stty cols $width                        # Set terminal width

#---------| Get opts |------------
until [[ -z $1 ]]; do case $1 in

    -server | -s) servers+=("$2");; # List of servers
    -update | -u) updates+=("$2");; # List of update files
    -script | -x) scripts+=("$2");; # List of script files
    -dump   | -m) dumps+=("$2");;   # List of dump files
    -job    | -j) jobs+=("$2");;    # List of cron job ids
    -date   | -d) date=$2;;         # Cron job date
    -cron   | -C) cron=$2;;         # Cron id set if running from cron
    -desc   | -D) desc=$2;;         # Show description instead of run
    -cmd    | -c) cmd=$2;;          # Command function to run
    -run    | -r) run=$2;;          # Command function to run from cron
    -key    | -k) key=$2;;          # Unique key
    -hid    | -h) hid=$2;;          # History id
    -cid    | -H) cid=$2;;          # Cronjob id
    -prj    | -p) prj=$2            # Project id:name
                  pname=${prj#*:}   # Project name
                  prj=${prj%:*};;   # Project id

esac; shift 2; done 2> /dev/null
#---------------------------------

# Write logs to DB
function make_history () {
    # Get DB configuration from conf.py
    raw=`grep 'db.* =' $workdir/../conf.py`
    raw=${raw//\'/}
    raw=${raw//=/}
    data=( $raw )

    declare -A dbconf # Create named array

    for ((i=0; i<${#data[*]}; i+=2)); do # loop through data
        key_value=( ${data[@]:$i:2} )    # get key_value pairs
        # assign  key___________________value pairs to named array
        dbconf["${key_value[0]}"]=${key_value[1]}
    done

    [[ $cid ]] && \
    job_update="UPDATE ups_job SET \"desc\" = \$$`cat $rundir/log$key`\$$ WHERE id = $cid AND proj_id = $prj;"
    PGPASSWORD=${dbconf[dbpass]} psql \
            -U ${dbconf[dbuser]} \
            -h ${dbconf[dbhost]} \
            -p ${dbconf[dbport]} \
            -d ${dbconf[dbname]} \
            -c "UPDATE ups_history SET \"desc\" = \$$`cat $rundir/log$key`\$$, exit = `cat $rundir/err$key`
                WHERE id = $hid AND proj_id = $prj;$job_update"
}

# Checks existence of updates/new folder in workdir, creates if not
function check_updates_folder () {
    printf "\n"
    ssh $sopt $addr "[[ -d $wdir/updates/new ]] || mkdir -p $wdir/updates/new" || error=$?
}

# Warning with countdown timer. Options: $1 - message, $2 - timeout in sec.
function warning () {
    attention=(
        '    _  _____ _____ _____ _   _ _____ ___ ___  _   _ _ '
        '   / \|_   _|_   _| ____| \ | |_   _|_ _/ _ \| \ | | |'
        '  / _ \ | |   | | |  _| |  \| | | |  | | | | |  \| | |'
        ' / ___ \| |   | | | |___| |\  | | |  | | |_| | |\  |_|'
        '/_/   \_\_|   |_| |_____|_| \_| |_| |___\___/|_| \_(_)'
        '                                                      ')

    for i in "${attention[@]}"; { info "$i"; }
    printf "\n\n$1"

    printf "If it's not what you wished to do, you've got $2 seconds to cancel this!\n"
    printf "Final countdown...\n"
    for i in $(seq $2); { sleep 1; echo $i; }
    printf "Ok, i warned you!)\n"
}

# Used in output log.
# Print delimiter line with info($1) in center.
function info () {
    [[ $2 ]]  && { [[ $2 = 0 ]] && F=':) ' || F=':( '; } # Add a smile to info if $2(error code) is set.
    #--------+-------------+--------------+------------+-----------------------+--------------------------------------+
    # Length | Body symbol | Start symbol | End symbol | Center part with info | Calculate number of body symbols     |
    #--------+-------------+--------------+------------+-----------------------+--------------------------------------+
    L=$width ; B='-'       ; S='<'        ; E='>'      ; C="{ $1 $F}"          ; b=$[(${L}-${#C}-${#S}-${#E})/2]
    #-------------------------------+--------------------------------+------------------------------------------------+
    # Make line segment.            | Calculate current length.      | Add one ${B} if current length less then ${L}. |
    #-------------------------------+--------------------------------+------------------------------------------------+
    N=$(printf %.s$B $(seq $b))     ; l=$[${#S}+${#C}+${#E}+${#N}*2] ; [[ $l -lt $L ]] && C+=$B
    printf "\n$S$N$C$N$E" # Print result.
}

# Server comes like this - jboss@localhost:/var/lib/jboss:8080
# This function splits it to: address, working directory and port
function addr () {
    #-----------------+-------------------+-----------------------------------+
    #    Ssh address  |      Bind port    |        Working directory          |
    #-----------------+-------------------+-----------------------------------+
    addr=${server%%:*}; port=${server##*:}; wdir=${server#*:}; wdir=${wdir%:*}

    # Cut ssh opts if exist
    testaddr=($addr); [[ ${#testaddr[*]} -gt 1 ]] && { sopt=${addr% *}; addr=${addr##* }; }

    # Show $addr as info
    info "Server $sopt $addr"
}

# If connecting first time send 'yes' on ssh's request.
# Expect must be installed on server. Options:
#   $1 - ssh address with parameters(if needed)
#
# Usage example:
#   ssh_yes "-p22 user@localhost"
function ssh_yes () {
expect << EOF
spawn ssh $1
expect {
    "(yes/no)?" {
        send "yes\n"
        expect {
            "assword:" { exit }
            "$ "       { send "exit\n" }
        }
    }
    "assword:" { exit }
    "$ "       { send "exit\n" }
}
exit
EOF
}

# Copy files created in the process to $dumpdir and add a 'download' button to the output log.
# Used in backup_* and dump_get.
function download () {
    [[ "$cron" ]] && { name=$(tail -n2 $crondir/$cron)  ; } \
                  || { name=$(tail -n2 $rundir/log$key) ; }
                       name=${name#*\"}; name=${name//\"./}

    ssh $sopt $addr [[ -f "$name" ]] && {

        newname=${addr}_${name//\/*\//}
        [[ -d $dumpdir/$1 ]] || mkdir $dumpdir/$1

        echo  -e "Копирую файл - ${name}"
        rsync -e "ssh $sopt" --progress -lzuogthvr $addr:$name $dumpdir/$1/$newname || error=$?
        case $1 in
            $pname) printf "\n<a class='btn btn-primary' href='/download_dump/$prj/$newname'>Download</a>\n";;
                '') printf "\n<b>File will be stored until tomorrow, please download it if you need this file!</b>"
                    printf "\n<a class='btn btn-primary' href='/dumps/$newname'>Download</a>\n";;
        esac

    } || { echo "File not found."; error=1; name=; }
}

# Load 'run' and 'description' functions from $cmd.
. $workdir/$cmd

# Start 'run' function, save logs to $rundir or $crondir if started from cron.
function starter  () {
    [[ "$cron" ]] && { run &> $crondir/$cron; dat=$(date +'%m.%d.%Y %R')
                       echo -e "\nError: ${error}\nDate: $dat" >> $crondir/$cron; } \
                  || { echo $$     > $rundir/pid$key
                       run        &> $rundir/log$key
                       echo $error > $rundir/err$key
                       [[ $hid ]] && make_history
                       sleep 2.5; rm $rundir/*$key; }
    exit $error
}

# Show description or run command itself
[[ "$desc" ]] && description || starter
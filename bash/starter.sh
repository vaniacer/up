#!/bin/bash

error=0                                 # Error
width=110                               # Output width
options=("$@")                          # Save all options in an array, needed for cron
workdir=$(dirname $0)                   # Work dir
cronfile=/var/spool/cron/crontabs/$USER # UpS user's crontab file
dumpdir=$workdir/../media/dumps         # Folder to store dumps
crondir=$workdir/../../logs/cron        # Folder to store cronjob logs
rundir=$workdir/../../logs/run          # Folder to store running tasks logs

#---------| Get opts |------------
until [[ -z $1 ]]; do case $1 in

    -update | -u) updates+=("$2");; # List of update files
    -script | -x) scripts+=("$2");; # List of script files
    -dump   | -m) dumps+=("$2");;   # List of dump files
    -job    | -j) jobs+=("$2");;    # List of cron job ids
    -server | -s) server="$2";;     # List of servers
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

# Print line, usage: line - 10 | line -= 20 | line "Hello World!" 20
line () { printf %.s"$1" $(seq $2); }

# Write logs to DB
function make_history () {

    [[ -f $rundir/log$key ]] || return

    log_lenght=(`cat $rundir/log$key | wc`)

    [[ $log_lenght -gt 50 ]] \
        && { LOG="<b>Log is too long to store in history, cutting...</b>"
             LOG="$LOG`head -n25 $rundir/log$key; printf "...\n"; tail -n25 $rundir/log$key`"; } \
        || { LOG=`cat $rundir/log$key`; }

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
    job_update="UPDATE ups_job SET \"desc\" = \$$ $LOG \$$ WHERE cron = '$cid' AND proj_id = $prj;"
    PGPASSWORD=${dbconf[dbpass]} psql \
            -U ${dbconf[dbuser]} \
            -h ${dbconf[dbhost]} \
            -p ${dbconf[dbport]} \
            -d ${dbconf[dbname]} \
            -c "UPDATE ups_history SET \"desc\" = \$$ $LOG \$$, exit = \$$ $error \$$
                WHERE uniq = '$key' AND proj_id = $prj;$job_update"
}

# Checks existence of updates/new folder in workdir, creates if not
function create_tmp_folder () {
    tmp_folder=$wdir/updates/new/$key
    ssh $sopt $addr "[[ -d $tmp_folder ]] || mkdir -p $tmp_folder" || error=$?
}

# Warning with countdown timer. Options: $1 - message, $2 - timeout in sec.
function warning () {

    attention=(
        '   _________________________________________________    '
        '  / __        ___    ____  _   _ ___ _   _  ____ _  \   '
        ' /  \ \      / / \  |  _ \| \ | |_ _| \ | |/ ___| |  \  '
        '/    \ \ /\ / / _ \ | |_) |  \| || ||  \| | |  _| |   \ '
        '\     \ V  V / ___ \|  _ <| |\  || || |\  | |_| |_|   / '
        ' \     \_/\_/_/   \_\_| \_\_| \_|___|_| \_|\____(_)  /  '
        '  \_________________________________________________/   ')

    for i in "${attention[@]}"; { printf "`line " " 32`$i\n"; }
    printf "\n$1"

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
    printf "\n$S$N$C$N$E\n" # Print result.
}

# Server comes like this - jboss@localhost:/var/lib/jboss:8080
# This function splits it to: address, working directory and port
function addr () {
    #-----------------+-------------------+-----------------------------------+------------------+
    #    Ssh address  |      Bind port    |        Working directory          | SSH option clear |
    #-----------------+-------------------+-----------------------------------+------------------+
    addr=${server%%:*}; port=${server##*:}; wdir=${server#*:}; wdir=${wdir%:*}; sopt=

    # Cut ssh opts if exist
    testaddr=($addr); [[ ${#testaddr[*]} -gt 1 ]] && { sopt=${addr% *}; addr=${addr##* }; }

    # Show $addr as info
    [[ $sopt ]] && mess="Server $sopt $addr" || mess="Server $addr"
    info "$mess"
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
    stty cols $width # Set terminal width
    [[ "$cron" ]] \
        && {
            run  &> $crondir/$cron;            dat=$(date +'%m.%d.%Y %R')
            echo -e "\nError: ${error}\nDate: $dat" >> $crondir/$cron
           } \
        || {
            echo $$     > $rundir/pid$key
            run        &> $rundir/log$key
            echo $error > $rundir/err$key
            sleep 2
            [[ $hid ]] && make_history
            sleep 2
            rm $rundir/*$key
           }
}

# Show description or run command itself
[[ "$desc" ]] && description || starter
exit $error
#!/bin/bash

error=0
options=("$@")
workdir=$(dirname $0)
cronfile=/var/spool/cron/crontabs/$USER
dumpdir=$workdir/../media/dumps
crondir=$workdir/../../logs/cron
rundir=$workdir/../../logs/run
#---------| Get opts |------------
until [ -z $1 ]; do case $1 in

    -server | -s) servers+=("$2");;
    -update | -u) updates+=("$2");;
    -script | -x) scripts+=("$2");;
    -dump   | -m) dumps+=("$2");;
    -job    | -j) jobs+=("$2");;
    -date   | -d) date=$2;;
    -cron   | -C) cron=$2;;
    -desc   | -D) desc=$2;;
    -cmd    | -c) cmd=$2;;
    -run    | -r) run=$2;;
    -key    | -k) key=$2;;
    -prj    | -p) prj=$2; pname=${prj#*:}; prj=${prj%:*};;

esac; shift 2; done 2> /dev/null
#---------------------------------

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
    L=120    ; B='-'       ; S='<'        ; E='>'      ; C="{ $1 $F}"          ; b=$[(${L}-${#C}-${#S}-${#E})/2]
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
# Expect must be installed on update server.
# $1 - ssh options, $2 - ssh address example:
# expect_ssh -p22 user@localhost
function expect_ssh () {
expect << EOF
spawn ssh $1 $2
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
        echo  -e "Копирую файл - ${name}"
        [[ -d $dumpdir/$pname ]] || mkdir $dumpdir/$pname

        rsync -e "ssh $sopt" --progress -lzuogthvr $addr:$name $dumpdir/$pname/$newname || error=$?
        echo  -e "\n<a class='btn btn-primary' href='/download_dump/$prj/$newname'>Download</a>\n"

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
                       echo $error > $rundir/err$key; }
    exit $error
}

# Show description or run command itself
[[ "$desc" ]] && description || starter
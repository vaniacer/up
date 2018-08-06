#!/bin/bash

confolder="$1"
filename="${2:-$dbname}_`printf "%(%d-%m-%Y)T"`.db.gz"

rawdta=$(grep '"DataaccessDS"' -A15 "$confolder"/jboss-bas-*/standalone/configuration/standalone-full.xml)
dbuser=${rawdta//*<user-name>/}; dbuser=${dbuser//<\/user-name>*/}
dbpass=${rawdta//*<password>/};  dbpass=${dbpass//<\/password>*/}
dbhost=${rawdta//*:\/\//};       dbhost=${dbhost//:[0-9]*/}
dbport=${rawdta//*${dbhost}:/};  dbport=${dbport//\/*/}
dbname=${rawdta//*${dbport}\//}; dbname=${dbname//<*/}
dbopts="-h $dbhost -p $dbport -U $dbuser"

PGPASSWORD="$dbpass" pg_dump -Ox $dbopts -d $dbname | gzip > "$filename" && printf "$filename" \
    || {
        error=$?
        printf "<b>Ошибка резервного копирования</b>"
        exit $error
       }
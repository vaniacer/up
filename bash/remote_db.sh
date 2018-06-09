#!/bin/bash

confolder="$1"

rawdta=$(grep '"DataaccessDS"' -A12 "$confolder"/jboss-bas-*/standalone/configuration/standalone-full.xml)
dbuser=${rawdta//*<user-name>/}; dbuser=${dbuser//<\/user-name>*/}
dbpass=${rawdta//*<password>/};  dbpass=${dbpass//<\/password>*/}
dbhost=${rawdta//*:\/\//};       dbhost=${dbhost//:[0-9]*/}
dbport=${rawdta//*${dbhost}:/};  dbport=${dbport//\/*/}
dbname=${rawdta//*${dbport}\//}; dbname=${dbname//<*/}
dbopts="-h $dbhost -p $dbport -U $dbuser"

filename="${2:-$dbname}_`printf "%(%d-%m-%Y)T"`.gz"

PGPASSWORD="$dbpass" pg_dump -Ox $dbopts -d $dbname | gzip > "$filename" || exit 1
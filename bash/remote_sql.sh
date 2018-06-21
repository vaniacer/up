#!/bin/bash

confolder="$1"
sqlscript="$2"

rawdta=$(grep '"DataaccessDS"' -A15 "$confolder"/jboss-bas-*/standalone/configuration/standalone-full.xml)
dbuser=${rawdta//*<user-name>/}; dbuser=${dbuser//<\/user-name>*/}
dbpass=${rawdta//*<password>/};  dbpass=${dbpass//<\/password>*/}
dbhost=${rawdta//*:\/\//};       dbhost=${dbhost//:[0-9]*/}
dbport=${rawdta//*${dbhost}:/};  dbport=${dbport//\/*/}
dbname=${rawdta//*${dbport}\//}; dbname=${dbname//<*/}
dbopts="-h $dbhost -p $dbport -U $dbuser"

PGPASSWORD="$dbpass" psql -v ON_ERROR_STOP=1 $dbopts $dbname < "$sqlscript" \
    || {
        error=$?
        printf "<b>Ошибка в скрипте - $sqlscript</b>"
        exit $error
       }
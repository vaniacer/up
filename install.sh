#!/bin/bash

admin=admin
paswd=1234qwer
email=marov@krista.ru

[[ -s conf.py ]] || { printf "\nCreate conf.py!\n\ncp conf.py{.template,}\n"; exit 1; }

printf "Install libs\n"
sudo apt-get update  -y
sudo apt-get install -y libpq-dev python-dev rsync expect ansible

printf "Add current user to crontab group to (un)set cron jobs\n"
sudo adduser $USER crontab

printf "Add virtual env\n"
virtualenv ../env; . ../env/bin/activate

printf "Create some folders\n"
mkdir -p static media/{dumps,scripts,updates} ../logs/{run,srv}

printf "Add logrotate\n"
logdir="`dirname $PWD`/logs/srv/*"
sudo cat > /etc/logrotate.d/ups << EOF
$logdir {
    weekly
    compress
    missingok
    rotate 12
    notifempty
    delaycompress
    create 0640 $USER $USER
}
EOF

printf "Install requirements\n"
easy_install $(cat requirements.txt)

printf "Create db and admin user\n"
./manage.py makemigrations ups; ./manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${admin}','${email}','${paswd}')" | \
    python manage.py shell

printf "Static files\n"
./manage.py collectstatic --noinput

printf "Test run\n"
./manage.py runserver
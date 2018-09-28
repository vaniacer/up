#!/bin/bash

admin=admin
paswd=1234qwer
email=marov@krista.ru

[ -s conf.py ] || { echo -e "Create 'conf.py' from 'conf.py.template'!"; exit 1; }

echo -e "Install libs."
sudo apt-get update  -y
sudo apt-get install -y libpq-dev python-dev rsync expect ansible

echo -e "Add current user to crontab group to (un)set cron jobs."
sudo adduser $USER crontab

echo -e "Add virtual env."
virtualenv ../env; . ../env/bin/activate

echo -e "Create some folders."
mkdir -p static media/{dumps,scripts,updates} ../logs/{run,srv}

echo -e "Add logrotate."
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

echo -e "Install requirements."
easy_install $(cat requirements.txt)

echo -e "Create db and admin user."
./manage.py makemigrations ups; ./manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${admin}','${email}','${paswd}')" | \
    python manage.py shell

echo -e "Static files."
./manage.py collectstatic --noinput

echo -e "Runserver."
./manage.py runserver
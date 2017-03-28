#!/bin/bash


admin=admin
paswd=1234qwer
email=marov@krista.ru

echo -e "Install libs."
sudo apt-get install -y libpq-dev python-dev

echo -e "Add virtual env."
virtualenv ../env
source ../env/bin/activate

echo -e "Create some folders."
mkdir static ../logs

echo -e "Install requirements."
easy_install $(cat requirements.txt)

echo -e "Create db and admin user."
./manage.py makemigrations ups
./manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${admin}','${email}','${paswd}')" | \
    python manage.py shell

echo -e "Static files."
./manage.py help collectstatic --noinput

echo -e "Runserver."
./manage.py runserver
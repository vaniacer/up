#!/bin/bash


admin=admin
paswd=1234qwer
email=marov@krista.ru

echo -e "Add virtual env."
virtualenv ../env
source ../env/bin/activate

echo -e "Install requirements."
easy_install $(cat requirements.txt)

echo -e "Create db and admin user."
./manage.py makemigrations ups
./manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${admin}','${email}','${paswd}')" | \
    python manage.py shell

echo -e "Runserver."
./manage.py runserver
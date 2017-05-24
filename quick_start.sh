#!/bin/bash

admin=admin
paswd=1234qwer
email=marov@krista.ru

echo -e "Install libs."
sudo apt-get install -y libpq-dev python-dev

echo -e "Add virtual env."
virtualenv ../env; . ../env/bin/activate

echo -e "Create some folders."
mkdir -p static media/updates/dumps ../logs/{cron,run,srv}

echo -e "Install requirements."
easy_install $(cat requirements.txt)

echo -e "Create db and admin user."
./manage.py makemigrations ups; ./manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${admin}','${email}','${paswd}')" | \
    python manage.py shell

echo -e "Static files."
./manage.py collectstatic --noinput

cd media/updates && ln -s ../../theme .theme; cd -
echo -e "\n\e[1mTo add download function please install nginx\e[0m:
    sudo apt-get install nginx

\e[1mAnd add following conf:\e[0m"
echo "
    server {

        listen 80;
        root ${PWD}/media;

        access_log  /var/log/nginx/updates.log;

        location / {
            fancyindex on;
            fancyindex_exact_size off;
            fancyindex_localtime  on;
            fancyindex_header   /updates/.theme/header.html;
            fancyindex_css_href /updates/.theme/style.css;
        }

        if (-f \$document_root/error503.html) { return 503; }

        error_page 503 @maintenance;

        location @maintenance { rewrite ^(.*)$ /error503.html break; }

        error_page  404  /404.html;

        location /404.html {
            root  /var/spool/www;
            rewrite ^(.*)$ /error404.html break;
        }
    }
"

echo -e "Runserver."
./manage.py runserver
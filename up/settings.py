# -*- encoding: utf-8 -*-

"""
Django settings for up project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from .conf import DATABASES, LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_L10N, USE_TZ, DEBUG


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRON_DIR = os.path.join(BASE_DIR, '../logs/cron/')
RUN_DIR = os.path.join(BASE_DIR, '../logs/run/')
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# Поддержка заголовка 'X-Forwarded-Proto' для request.is_secure().
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '20)3uo!@xp0@^2ljzw)%@s^3%gq_f(e8usbe2(g@pz*3x^btfs'


# ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['localhost']
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# Мои приложения
	'users',
	'ups',
	# mods
	'bootstrap3',
	'guardian',
	'pytz',
	'dj_database_url',
	'dj_static',
	'psycopg2',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'up.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'ups/templates/ups')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'up.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
	]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# Мои настройки
LOGIN_URL = '/users/login/'

# Настройки django-bootstrap3
BOOTSTRAP3 = {
	'include_jquery': True,
}

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',  # this is default
	'guardian.backends.ObjectPermissionBackend',
)

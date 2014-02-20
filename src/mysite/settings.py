"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@4hf=&8n&(4ch(8q4@r%_^0*^p+k4j1m*@5&$y2%u1m*thrh(3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

CUR_DIR=os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(CUR_DIR,'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = './media/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
		'mysite.books',
		'mysite.contact',
    'mysite.tables',
    'mysite.ADAdmin',
    'django_tables2',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
	os.path.join(os.path.dirname(__file__), 'ADAdmin/templates').replace('\\','/'),
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'

'''
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)
'''

TEMPLATE_LOADERS = (
    'django.template.loaders.eggs.Loader',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE':'django.db.backends.mysql',
    'NAME': 'test_db',
    'USER': 'mysql_admin',
    'PASSWORD': '123',
    'HOST': 'localhost',
    'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

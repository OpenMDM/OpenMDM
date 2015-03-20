"""
Django settings for OpenMDM project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ldap
from common.local.settings import *
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType
from mongoengine import connect


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7d0q=o@j-qmq=u09$p%6cq03))+%&qfvz+gbw^^y2y_5pa7&v&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
    'public_gate',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    # 'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'OpenMDM.urls'

WSGI_APPLICATION = 'OpenMDM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


DATABASES = {
    'default': CONFIG['local']['database']
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'src'),
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# plist group

RETRIEVE_PLIST_FROM_GROUPS = "all"
# RETRIEVE_PLIST_FROM_GROUPS = "first"

# LDAP

AUTH_LDAP_SERVER_URI = CONFIG['local']['ldap']['SERVER_URI']
# Diect bind
# AUTH_LDAP_USER_DN_TEMPLATE = "cn=%(user)s,ou=users,dc=ldap,dc=hackndo,dc=com"
# Search / Bind
AUTH_LDAP_BIND_DN = CONFIG['local']['ldap']['BIND_DN']
AUTH_LDAP_BIND_PASSWORD = CONFIG['local']['ldap']['BIND_PASSWORD']
AUTH_LDAP_USER_SEARCH = CONFIG['local']['ldap']['USER_SEARCH']

# Finding groups
AUTH_LDAP_GROUP_SEARCH = CONFIG['local']['ldap']['GROUP_SEARCH']
AUTH_LDAP_GROUP_TYPE = CONFIG['local']['ldap']['GROUP_TYPE']
AUTH_LDAP_REQUIRE_GROUP = CONFIG['local']['ldap']['REQUIRE_GROUP']

connect(CONFIG['local']['mongo']['DB'])
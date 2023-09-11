import os

from .common import *

import dj_database_url

from dotenv import load_dotenv

# Loading environment variable's
load_dotenv()

# Django secret key
SECRET_KEY = os.environ.get('SECRET_KEY')

# Enable sever mode
DEBUG = False

# Allowed run server in this host
HOST = os.environ.get('HOST')
ALLOWED_HOSTS = ['127.0.0.1', HOST]

# Final database
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL')),
}


# Configure Cache system
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 604800  # 7 Days
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# CSRF Attack
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# XSS Attack
SECURE_BROWSER_XSS_FILTER = True
SECURE_COUNT_TYPE_NOSNIFF = True

# ENABLE HSTS
SECURE_HSTS_SECONDS = 86400 # 1 day
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SSL Redirect
SECURE_SSL_REDIRECT = True

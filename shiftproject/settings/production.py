from .base import *

SECTRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = ['.herokuapp.com']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

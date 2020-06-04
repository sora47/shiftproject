from .base import *

SECTRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

from dj_database_url import config
db_from_env = config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = ['.herokuapp.com']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

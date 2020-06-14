from fintrack.settings.common import *
from fintrack.settings.secret_key import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Your local host IP
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'LOCAL DATABASE NAME',
        'USER': 'LOCAL DATABASE USER',
        'PASSWORD': 'LOCAL DATABASE PASSWORD',
        # Only change these if you have configured manually
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_USE_TLS = True
# Your local test email host, below is Googles example
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'EMAIL ADDRESS'
EMAIL_HOST_PASSWORD = 'EMAIL ADDRESS PASSWORD'
EMAIL_PORT = 'EMAIL PORT'

# Change depending on your local Redis configuration
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# These settings dont need to be changed
CELERY_BROKER_URL = os.environ.get(
    'REDIS_URL', 'redis://{host}:{port}/0'.format(host=REDIS_HOST, port=str(REDIS_PORT)))
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_PREFETCH_MULTIPLIER = 1

CORS_ORIGIN_ALLOW_ALL = True

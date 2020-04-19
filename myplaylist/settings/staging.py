from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


CELERY_BROKER_URL = 'amqp://localhost'

RABBITMQ_URL = 'amqp://guest:guest@localhost'
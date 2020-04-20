from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']




DATABASES = {
		'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'myplaylist_rds',
		'USER': 'postgres',
		'PASSWORD': 'postgres',
		'HOST': 'myplaylist-rds.cuyk4lxvhrqe.ap-south-1.rds.amazonaws.com',
		'PORT': '5432',
		}
}

# BROKER_URL = 'amqp://localhost'
# BROKER_HEARTBEAT = 40

# RABBITMQ_URL = 'amqp://guest:guest@localhost'
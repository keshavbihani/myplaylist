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

BROKER_URL = 'amqp://qhfoemfx:XXeIkg9oXCRUT8Ej-yfLZt2x9n4dVqNa@eagle.rmq.cloudamqp.com/qhfoemfx'
BROKER_HEARTBEAT = 40

RABBITMQ_URL = 'amqp://qhfoemfx:XXeIkg9oXCRUT8Ej-yfLZt2x9n4dVqNa@eagle.rmq.cloudamqp.com/qhfoemfx'
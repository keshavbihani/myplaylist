import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myplaylist.settings.local')
django.setup()
import pika
from django.conf import settings
import json
from music.models import UserPlayingMapping

def user_update(msg):
  if msg:
    import ipdb
    ipdb.set_trace()
    data = json.loads(msg.decode())
    user = UserPlayingMapping.objects.filter(user_id = data.get('id')).last()
    if user:
        user.username = data.get('username')
        user.save()
    else:
         UserPlayingMapping.objects.create(user_id = data.get('id'),
                                            username= data.get('username'))   
  return;



class PikaConsumer:

    def __init__(self,url=None,queue_name=None,function_name=None):
        try:
            self.url = url if url else settings.RABBITMQ_URL
            self.queue_name = queue_name
            self.function_name = function_name
            params = pika.URLParameters(self.url)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel() # start a channel
            self.channel.queue_declare(queue=queue_name) # Declare a queue
            self.subscribe()
        except pika.exceptions.ConnectionClosedByBroker:
            print('connection broke by broker')
        except pika.exceptions.AMQPChannelError:
            print('channel error')
        except pika.exceptions.AMQPConnectionError:
            print('error un amqp connection')

    def callback(self,ch, method, properties, body):
        eval(self.function_name)(body)

    def subscribe(self):
        self.channel.basic_consume(self.queue_name,
              self.callback,
              auto_ack=True)        

    
    def consume(self):
        while True:
            try:
                self.channel.start_consuming()  
            except KeyboardInterrupt:
                self.close()    

    def close(self):        
        self.connection.close()   


if __name__ == "__main__":
    PikaConsumer(queue_name='user-queue',function_name='user_update').consume()
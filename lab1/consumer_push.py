from custom_serializer import MessageDeserializer
from confluent_kafka import KafkaException
from confluent_kafka import DeserializingConsumer

msg_deserializer = MessageDeserializer()

config = {
    'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092', 
    'group.id': 'group_push',
    'auto.offset.reset': 'earliest', # начальное значение offset если группы с id = group_push не существует
    'value.deserializer': msg_deserializer, # для десериализации сообщений
    'enable.auto.commit': True # автоматическое подтверждение offset. Хотя оно и так стоит по умолчанию, 
}

consumer_push = DeserializingConsumer(config)
consumer_push.subscribe(['lab.topic'])

while True:
    message = consumer_push.poll(timeout=1.0)
    if not message:
        continue
    if message.error():
        print(f'Failed to {message.error()}')
        KafkaException(message.error())
    else:
        print(message.value())

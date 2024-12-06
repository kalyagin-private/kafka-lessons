import time
from message import Message
from custom_serializer import MessageSerializer
from confluent_kafka import SerializingProducer


msg_converter = MessageSerializer()

config = {
    'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092',
    'client.id': 'python-producer',
    'value.serializer': msg_converter, # Требуется для серилиазации сообщений
    'acks': 1, # Required for at least once delivery
    'retries': 3 # Количесво попытток отправить сообщение в кафку
}

producer = SerializingProducer(config)


def send_message(topic, message):
    try:
        print(f'Message "{message}" sending...') # для простого debugging
        producer.produce(topic, value=message)
    except Exception as e:
        print("Error while sending message")
        print(e)


try:
    message_for_send = Message(1, "test_message_kafka", 200)
    while True:
        send_message("lab.topic", message_for_send)
        time.sleep(2) # Пауза в 2 секунды, просто чтобы не заваливать сообщениями
except KeyboardInterrupt:
    print("Stopped.")
    producer.flush()

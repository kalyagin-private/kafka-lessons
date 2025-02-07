import time
import random
import json
import logging
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer

logging.getLogger().setLevel(logging.INFO)


def generate_massage():
    return json.dumps(
        {
            "Alloc": {
                "Type": "gauge",
                "Name": "Alloc",
                "Description": "Alloc is bytes of allocated heap objects.",
                "Value": random.randrange(20000000, 40000000),
            },
            "FreeMemory": {
                "Type": "gauge",
                "Name": "FreeMemory",
                "Description": "RAM available for programs to allocate",
                "Value": random.randrange(8000000000, 16000000000),
            },
            "PollCount": {
                "Type": "counter",
                "Name": "PollCount",
                "Description": "PollCount is quantity of metrics collection iteration.",
                "Value": random.randrange(1, 4),
            },
            "TotalMemory": {
                "Type": "gauge",
                "Name": "TotalMemory",
                "Description": "Total amount of RAM on this system",
                "Value": random.randrange(8000000000, 16000000000),
            },
        }
    )


msg_converter = StringSerializer()

config = {
    "bootstrap.servers": "kafka:9092",
    "client.id": "metrics-producer",
    "value.serializer": msg_converter,  # Требуется для серилиазации сообщений
    "acks": 1,  # Required for at least once delivery
    "retries": 3,  # Количесво попытток отправить сообщение в кафку
}

producer = SerializingProducer(config)


def send_message(topic, message):
    try:
        logging.info(f'Message "{message}" sending...')  # для простого debugging
        producer.produce(topic, value=message)
    except Exception as e:
        logging.error("Error while sending message")
        logging.error(e)


try:
    while True:
        message_for_send = generate_massage()
        send_message("metrics-topic", message_for_send)
        time.sleep(5)  # Пауза в 5 с, просто чтобы не заваливать сообщениями
except KeyboardInterrupt:
    logging.info("Stopped.")
    producer.flush()

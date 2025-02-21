import logging
import time
import os
from confluent_kafka import Producer

logging.getLogger().setLevel(logging.INFO)


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "kafka-0:9092,kafka-1:9092,kafka-2:9092"
)
SSL_CERT_LOC = os.getenv("SSL_CERT_LOC", "secrets/kafka-1.crt")
SSL_KEY_NAME = os.getenv("SSL_KEY_NAME", "secrets/kafka-1.key")
SASL_USER = os.getenv("SASL_USER")
SASL_PASSWORD = os.getenv("SASL_PASSWORD")


config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "client.id": "app-producer",
    "acks": 1,  # Required for at least once delivery
    "retries": 3,  # Количесво попытток отправить сообщение в кафку
    # Настройки безопасности SSL
    "security.protocol": "SASL_SSL",
    "ssl.ca.location": "secrets/ca.crt",  # Сертификат центра сертификации
    "ssl.certificate.location": SSL_CERT_LOC,  # Сертификат клиента Kafka
    "ssl.key.location": SSL_KEY_NAME,  # Приватный ключ для клиента Kafka
    # Настройки SASL-аутентификации
    "sasl.mechanism": "PLAIN",  # Используемый механизм SASL (PLAIN)
    "sasl.username": SASL_USER,  # Имя пользователя для аутентификации
    "sasl.password": SASL_PASSWORD,  # Пароль пользователя для аутентификации
}

logging.info(config)

producer = Producer(config)


def send_message(topic, message):
    try:
        logging.info(f'Message "{message}" sending...')  # для простого debugging
        producer.produce(topic, value=message)
    except Exception as e:
        logging.error("Error while sending message")
        logging.error(e)


try:
    while True:
        send_message("app-topic", "message_for_send")
        time.sleep(5)  # Пауза в 5 с, просто чтобы не заваливать сообщениями
except KeyboardInterrupt:
    logging.info("Stopped.")
    producer.flush()

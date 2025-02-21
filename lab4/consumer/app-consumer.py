import logging
import os
from confluent_kafka import KafkaException
from confluent_kafka import Consumer

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
    "group.id": "app-group",
    "auto.offset.reset": "earliest",  # начальное значение offset если группы с id = group_push не существует
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

consumer = Consumer(config)
consumer.subscribe(["app-topic"])

while True:
    try:
        message = consumer.poll(timeout=2.0)
    except KafkaException as e:
        logging.error(f"Failed to {e}")

    if not message:
        continue
    if message.error():
        logging.error(f"Failed to {message.error()}")
        KafkaException(message.error())
    else:
        logging.info(f"Received message: {message.value()}")

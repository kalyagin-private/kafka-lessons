import argparse
import time
import json
import logging
from confluent_kafka import Producer

logging.getLogger().setLevel(logging.INFO)

config = {
    "bootstrap.servers": "localhost:19092,localhost:29092,localhost:39092",
    "client.id": "message-sender",
    "acks": 1,  # Required for at least once delivery
    "retries": 3,  # Количесво попытток отправить сообщение в кафку
}

producer = Producer(config)

msg = {
    "from_user_id": 1,
    "to_user_id": 2,
    "ts": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    "message": "Привет, как твои дела, некрасивый, малоко хорошо",
}


def send_message(topic, message):
    try:
        logging.info(f'Message "{message}" sending...')  # для простого debugging
        producer.produce(topic, value=message)
    except Exception as e:
        logging.error(f"Error while sending message \n {e}")


# Для тестов в атоматическом режиме
# try:
#     message_for_send = json.dumps(msg).encode("utf-8")
#     while True:
#         send_message("messages", message_for_send)
#         time.sleep(3)  # Пауза в 3 секунды, просто чтобы не заваливать сообщениями
# except KeyboardInterrupt:
#     logging.info("Stopped.")
#     producer.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--from_id", required=True)
    parser.add_argument("--to_id", required=True)
    parser.add_argument("--msg", required=True)
    args = parser.parse_args()
    msg = {
        "from_user_id": args.from_id,
        "to_user_id": args.to_id,
        "ts": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "message": args.msg,
    }
    message_for_send = json.dumps(msg).encode("utf-8")
    send_message("messages", message_for_send)
    producer.flush()

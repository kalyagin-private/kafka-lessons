import time
from custom_serializer import MessageDeserializer
from confluent_kafka import KafkaException
from confluent_kafka import DeserializingConsumer

msg_deserializer = MessageDeserializer()

config = {
    "bootstrap.servers": "localhost:19092,localhost:29092,localhost:39092",
    "group.id": "group_pull",
    "auto.offset.reset": "earliest",
    "value.deserializer": msg_deserializer,
    "enable.auto.commit": False,
}

consumer_pull = DeserializingConsumer(config)
consumer_pull.subscribe(["lab.topic"])


"""
внутри poll используется timeout и имеется внутренний бесконечный цикл, поэтому именно как "паузу"
между забором данных использовать не получится, то есть если сообщения появляются "нонстопом", 
то и в этом случае будет бесконечный поток сообщений.

Для имитации именно некого шедуленга, что мы забираем раз в 5 секунд все накопившиеся сообщения в топике
используем метод time.sleep(5).
"""
f = open("consumed_messages.txt", "a+")
while True:
    message = consumer_pull.poll(timeout=1.0) 
    if not message:
        continue
    if message.error():
        print(f"Failed to {message.error()}")
        KafkaException(message.error())
    else:
        f.write(str(message.value()) + "\n")
        consumer_pull.commit() # после записи в файл сами подтвердаем смещенеи offset в топике
        print(f"Consumed {message.value()}")
    time.sleep(5)
f.close()

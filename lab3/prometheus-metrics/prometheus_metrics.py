from fastapi.responses import PlainTextResponse
import uvicorn
import json
import logging
from fastapi import FastAPI, Body
from confluent_kafka import KafkaException
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka import DeserializingConsumer
from templating import render_metrics

# Global переменные для хранения последних полученных метрик. При каждом запуске приложения они будут перезаписаны.
# Да, global переменные лучше не использовать, но все же для простоты реализации и не усложнения проекта решение в лоб.
last_metrics = None
consumer = None
cfg = None

logging.getLogger().setLevel(logging.INFO)

app = FastAPI()


# Класс отдельный, для эмуляции некого хранилища. При использовании Kafka-connect хранит данные в 3х топиках.
# Так как это не полноценный коннектор, а лишь некий сервис похожий на Kafka-connect, то будет такое допущение.
class Config:
    def __init__(self, name, topic, bootstrap, prometheus_listener_url, group_id):
        self.name = name
        self.topic = topic
        self.bootstrap = bootstrap
        self.type = "sink"
        self.state = "RUNNING"
        self.worker_id = "127.0.0.1"
        self.prometheus_listener_url = prometheus_listener_url
        self.group_id = group_id


@app.get("/")
def root_route():
    return "Эмуляция Kafka-connect"


@app.get("/metrics", response_class=PlainTextResponse)
def get_metrics():
    global last_metrics
    if consumer is None:
        logging.info("No consumer")
        return
    try:
        message = consumer.poll(timeout=2.0)
    except KafkaException as e:
        logging.error(f"Failed to {e}")

    if message is None:
        logging.info("No message received")
        return render_metrics(last_metrics)
    if message.error():
        logging.error(f"Failed to {message.error()}")
        KafkaException(message.error())
    else:
        json_message = json.loads(message.value())
        consumer.commit(message=message)
        last_metrics = json_message
        prometheus_metric = render_metrics(json_message)
        logging.info(prometheus_metric)
    return prometheus_metric


@app.get("/connectors/{connector_name}/status")
def get_status(connector_name: str):
    if cfg.name == connector_name:
        status = {
            "name": cfg.name,
            "connector": {"state": cfg.state, "worker_id": cfg.worker_id},
            "tasks": [{"id": 0, "state": cfg.state, "worker_id": cfg.worker_id}],
            "type": cfg.type,
        }
        return status


@app.post("/connectors")
def put_connectors(data=Body()):
    global cfg
    if cfg is None:
        cfg = Config(
            name=data["name"],
            topic=data["topics"],
            bootstrap=data["confluent.topic.bootstrap.servers"],
            prometheus_listener_url=data["prometheus.listener.url"],
            group_id=data["group.id"],
        )
    msg_deserializer = StringDeserializer()

    config = {
        "bootstrap.servers": data["confluent.topic.bootstrap.servers"],
        "group.id": data["group.id"],
        "auto.offset.reset": "earliest",
        "value.deserializer": msg_deserializer,
        "enable.auto.commit": True,
    }
    global consumer
    if consumer is not None:
        print("Stoping prev consumer.")
        consumer.close()
    consumer = DeserializingConsumer(config)
    consumer.subscribe(["metrics-topic"])
    return f"{data}"


@app.put("/connectors/{connector_name}/config")
def put_connector_config(data=Body()):
    global cfg
    if cfg is None:
        cfg = Config(
            name=data["name"],
            topic=data["topics"],
            bootstrap=data["confluent.topic.bootstrap.servers"],
            prometheus_listener_url=data["prometheus.listener.url"],
            group_id=data["group.id"],
        )
    msg_deserializer = StringDeserializer()

    config = {
        "bootstrap.servers": data["confluent.topic.bootstrap.servers"],
        "group.id": data["group.id"],
        "auto.offset.reset": "earliest",
        "value.deserializer": msg_deserializer,
        "enable.auto.commit": True,
    }
    global consumer
    if consumer is not None:
        logging.info("Stoping prev consumer.")
        consumer.close()
    consumer = DeserializingConsumer(config)
    consumer.subscribe(["metrics-topic"])
    return f"{data}"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8383)

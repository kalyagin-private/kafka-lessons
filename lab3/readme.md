# Список файлов и их краткое описание

* docker-compose.yaml - docker compose файл, содержащий все необходимые сервисы для работы (kakfa+zookeeper+kafka-ui и т.д.)
* deploy-jdbc-sink.sh - bash скрипт для создания топика, а так же вывода информации о созданном топике
* prometheus.yaml - Содержит конфиг для агентов prometheus
* plugins - папка с plugins для kafka-connect
* grafana - папка с конфигами и дашбордом для Grafana
* kafka-connect - папка содержит кофиги (jdbc-source, debezium connect) для kafka-connect, а так же конфиги и экспортер JMX метрик.   
* prometheus-metrics - папка содержит все необходимо для реализации сервиса вычитки из кафки сообщений, и предоствление из через api для агентов prometheus:
  - producer_metrics.py - простой продюсер, для отправки сообщений в топик кафку - эмуляция генерации метрик
  - templating.py - небольшой модуль для преобразования сообщений из кафка в формат prometheus
  - prometheus_metrics.py - основной модуль сервиса в рамках которого реализован вебсервер и несколькими endpoints
  - Dockerfile - для создания образа разраотанного сервиса, чтобы он разворачивался вместе со всеми компонентами
  - *.json - файлы с примерами из задания

# Описание

Для работы необходимо поднять docker compose:
```shell
docker compose up -d
```
Для проверки что кафка коннект работает корректно и есть необходимые плагины выполнил curl
```shell
$ curl localhost:8083/connector-plugins | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1201  100  1201    0     0  19912      0 --:--:-- --:--:-- --:--:-- 20016
[
  {
    "class": "com.github.markteehan.file.chunk.sink.ChunkSinkConnector",
    "type": "sink",
    "version": "null"
  },
  {
    "class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "type": "sink",
    "version": "10.8.0"
  },
  {
    "class": "io.confluent.connect.s3.S3SinkConnector",
    "type": "sink",
    "version": "10.5.13"
  },
  {
    "class": "io.debezium.connector.jdbc.JdbcSinkConnector",
    "type": "sink",
    "version": "2.7.3.Final"
  },
  {
    "class": "org.apache.kafka.connect.file.FileStreamSinkConnector",
    "type": "sink",
    "version": "7.7.0-ccs"
  },
  {
    "class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "type": "source",
    "version": "10.8.0"
  },
  {
    "class": "io.confluent.connect.storage.tools.SchemaSourceConnector",
    "type": "source",
    "version": "7.7.0-ccs"
  },
  {
    "class": "io.debezium.connector.postgresql.PostgresConnector",
    "type": "source",
    "version": "2.5.4.Final"
  },
  {
    "class": "org.apache.kafka.connect.file.FileStreamSourceConnector",
    "type": "source",
    "version": "7.7.0-ccs"
  },
  {
    "class": "org.apache.kafka.connect.mirror.MirrorCheckpointConnector",
    "type": "source",
    "version": "7.7.0-ccs"
  },
  {
    "class": "org.apache.kafka.connect.mirror.MirrorHeartbeatConnector",
    "type": "source",
    "version": "7.7.0-ccs"
  },
  {
    "class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
    "type": "source",
    "version": "7.7.0-ccs"
  }
]
```


Для добавления необходимых коннекторов в kafka-connector
```shell
./deploy-jdbc-sink.sh
```

Для начала отправки сообщений с метриками необходимо запустить producer_metrics.py
В результате мы отправим несколько сообщений в топик metrics-producer для последующей обработки кансамером и отправкой в прометеус
```shell
$ python prometheus-metrics/producer_metrics.py
Message "{"Alloc": {"Type": "gauge", "Name": "Alloc", "Description": "Alloc is bytes of allocated heap objects.", "Value": 25406900}, "FreeMemory": {"Type": "gauge", "Name": "FreeMemory", "Description": "RAM available for programs to allocate", "Value": 14021908462}, "PollCount": {"Type": "counter", "Name": "PollCount", "Description": "PollCount is quantity of metrics collection iteration.", "Value": 1}, "TotalMemory": {"Type": "gauge", "Name": "TotalMemory", "Description": "Total amount of RAM on this system", "Value": 8345511048}}" sending...
Message "{"Alloc": {"Type": "gauge", "Name": "Alloc", "Description": "Alloc is bytes of allocated heap objects.", "Value": 34439890}, "FreeMemory": {"Type": "gauge", "Name": "FreeMemory", "Description": "RAM available for programs to allocate", "Value": 11871473182}, "PollCount": {"Type": "counter", "Name": "PollCount", "Description": "PollCount is quantity of metrics collection iteration.", "Value": 3}, "TotalMemory": {"Type": "gauge", "Name": "TotalMemory", "Description": "Total amount of RAM on this system", "Value": 10067911613}}" sending...
Message "{"Alloc": {"Type": "gauge", "Name": "Alloc", "Description": "Alloc is bytes of allocated heap objects.", "Value": 39858699}, "FreeMemory": {"Type": "gauge", "Name": "FreeMemory", "Description": "RAM available for programs to allocate", "Value": 15708212496}, "PollCount": {"Type": "counter", "Name": "PollCount", "Description": "PollCount is quantity of metrics collection iteration.", "Value": 1}, "TotalMemory": {"Type": "gauge", "Name": "TotalMemory", "Description": "Total amount of RAM on this system", "Value": 11397058424}}" sending...
Message "{"Alloc": {"Type": "gauge", "Name": "Alloc", "Description": "Alloc is bytes of allocated heap objects.", "Value": 31609960}, "FreeMemory": {"Type": "gauge", "Name": "FreeMemory", "Description": "RAM available for programs to allocate", "Value": 9642928506}, "PollCount": {"Type": "counter", "Name": "PollCount", "Description": "PollCount is quantity of metrics collection iteration.", "Value": 2}, "TotalMemory": {"Type": "gauge", "Name": "TotalMemory", "Description": "Total amount of RAM on this system", "Value": 11903018376}}" sending...
Message "{"Alloc": {"Type": "gauge", "Name": "Alloc", "Description": "Alloc is bytes of allocated heap objects.", "Value": 22736434}, "FreeMemory": {"Type": "gauge", "Name": "FreeMemory", "Description": "RAM available for programs to allocate", "Value": 9047411041}, "PollCount": {"Type": "counter", "Name": "PollCount", "Description": "PollCount is quantity of metrics collection iteration.", "Value": 2}, "TotalMemory": {"Type": "gauge", "Name": "TotalMemory", "Description": "Total amount of RAM on this system", "Value": 11697398922}}" sending...
Message "{"Alloc": {"Type": "gauge", "Name": "Alloc", "Description": "Alloc is bytes of allocated heap objects.", "Value": 21078182}, "FreeMemory": {"Type": "gauge", "Name": "FreeMemory", "Description": "RAM available for programs to allocate", "Value": 13321056464}, "PollCount": {"Type": "counter", "Name": "PollCount", "Description": "PollCount is quantity of metrics collection iteration.", "Value": 1}, "TotalMemory": {"Type": "gauge", "Name": "TotalMemory", "Description": "Total amount of RAM on this system", "Value": 15540771974}}" sending...
Stopped.
```



Для запуска сервиса по выгрузки сообщений из Kafka в Prometheus
```shell
$ python prometheus-metrics/prometheus_metrics.py
INFO:     Started server process [9272]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8383 (Press CTRL+C to quit)
```


Для настройки севрсиса необходимо отправить конфигурацию, котрая похожа на конфиг kafka-connect
```shell
curl -X POST -H "Content-Type:application/json" --data @prometheus-metrics/config.json http://localhost:8383/connectors | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   528  100   255  100   273   2959   3168 --:--:-- --:--:-- --:--:--  6211
"{'name': 'prometheus-connector', 'topics': 'metrics-producer', 'group.id': 'group-metrics-1', 'confluent.topic.bootstrap.servers': 'kafka:9092', 'prometheus.listener.url': 'http://localhost:8383/metrics', 'reporter.result.topic.replication.factor': '1'}"
```
где http://localhost:8383 - это адрес и порт разработанного сервиса. Данный сервис поднят тоже через docker compose, чтобы все сервисы работали в единой сети


Для проверки того что сервис запущен и отдает метрики можно выполнить команду
```shell
$ curl localhost:8383/metrics
# HELP Alloc Alloc is bytes of allocated heap objects.
# TYPE Alloc gauge
Alloc 21078182
# HELP FreeMemory RAM available for programs to allocate
# TYPE FreeMemory gauge
FreeMemory 13321056464
# HELP PollCount PollCount is quantity of metrics collection iteration.
# TYPE PollCount counter
PollCount 1
# HELP TotalMemory Total amount of RAM on this system
# TYPE TotalMemory gauge
TotalMemory 15540771974
```

Проверяем агента в прометеус. должена быть соответствующая настройка в prometheus.yaml
```yaml
    # Scrape custom /metrics
  - job_name: 'Custom-kafka-connect'
    static_configs:
      - targets: ['custom-kafka-connect:8383']
```
Проверить сам прометеус можно черз UI. Примеры скриншотов в соответствующей папке.

Так же можно проверить статус кастомного коннектора:
```shell
$ curl localhost:8383/connectors/prometheus-connector/status | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   162  100   162    0     0   4221      0 --:--:-- --:--:-- --:--:--  4263
{
  "name": "prometheus-connector",
  "connector": {
    "state": "RUNNING",
    "worker_id": "127.0.0.1"
  },
  "tasks": [
    {
      "id": 0,
      "state": "RUNNING",
      "worker_id": "127.0.0.1"
    }
  ],
  "type": "sink"
}
```

# Краткие замечания

* Так как реализовать через Python полноценный kafka коннектор нет возможности, то тут
получается реализация отдельного сервиса, внутри которого работает обычный кансамер, который вычитывает данные из топика при образщении на определенный endpoint.
* Многие вещи при реализации упрощены, т.к. это некторое PoC.



# Результаты эксперементов с ускорением JDBC Source

| Поле 1 | batch.max.rows | batch.size | linger.ms | Скорость записи |
---------|----------------|------------|-----------|-----------------|
| Поле 1 | 100            | 18400      | 1000      | 152k op/s       |
| Поле 1 | 1000           | 18400      | 1000      | 152k            |
| Поле 1 | 100            | 500        | 1000      | 19-20к             |
| Поле 1 | 1000           | 184000     | 1000      | 19к             |



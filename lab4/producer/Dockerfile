FROM python:3.11-slim

WORKDIR /opt/custom-app

COPY app-producer.py /opt/custom-app/

RUN apt-get update && \
pip install kafka confluent-kafka && \
mkdir /opt/custom-app/secrets

CMD [ "python", "/opt/custom-app/app-producer.py" ]

FROM python:3.11-slim

WORKDIR /opt/custom-app

COPY templating.py prometheus_metrics.py /opt/custom-app/

RUN apt-get update && \
pip install fastapi uvicorn kafka jinja2 confluent-kafka

CMD [ "python", "/opt/custom-app/prometheus_metrics.py" ]
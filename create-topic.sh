

CONTAINER_NAME="kafka-1"    
BOOTSTRAP_SERVERS="kafka-1:9092"

docker exec -it "$CONTAINER_NAME" kafka-topics \
    --bootstrap-server $BOOTSTRAP_SERVERS \
    --create \
    --topic lab.topic \
    --partitions 3 \
    --replication-factor 2


docker exec -it "$CONTAINER_NAME" kafka-topics \
    --bootstrap-server $BOOTSTRAP_SERVERS \
    --topic lab.topic \
    --describe 
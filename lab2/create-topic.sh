CONTAINER_NAME="kafka-1"    
BOOTSTRAP_SERVERS="kafka-1:9092"

docker exec -it "$CONTAINER_NAME" kafka-topics \
    --bootstrap-server $BOOTSTRAP_SERVERS \
    --create \
    --topic messages \
    --partitions 1 \
    --replication-factor 2

docker exec -it "$CONTAINER_NAME" kafka-topics \
    --bootstrap-server $BOOTSTRAP_SERVERS \
    --create \
    --topic filtered_messages \
    --partitions 1 \
    --replication-factor 2

docker exec -it "$CONTAINER_NAME" kafka-topics \
    --bootstrap-server $BOOTSTRAP_SERVERS \
    --create \
    --topic censor_messages \
    --partitions 1 \
    --replication-factor 2

#!/bin/bash 

curl -X PUT -H "Content-Type:application/json" --data @kafka-connect/jdbc-source-trans.json http://localhost:8083/connectors/jdbc-source-trans/config
curl -X PUT -H "Content-Type:application/json" --data @kafka-connect/reg-postgres.json http://localhost:8083/connectors/reg-postgres/config

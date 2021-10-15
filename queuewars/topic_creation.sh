#!/bin/bash

KAFKA_HOME="kafka"
ZK="--zookeeper localhost:2181"

NUM_PART=$1

TOPIC_CHUNKS=chunks
TOPIC_CONFIRMED=confirmed
TOPIC_UNRESOLVED=unresolved

$KAFKA_HOME/bin/kafka-topics.sh $ZK --create --replication-factor 1 --partitions $NUM_PART --topic $TOPIC_CHUNKS
$KAFKA_HOME/bin/kafka-topics.sh $ZK --create --replication-factor 1 --partitions $NUM_PART --topic $TOPIC_CONFIRMED
$KAFKA_HOME/bin/kafka-topics.sh $ZK --create --replication-factor 1 --partitions $NUM_PART --topic $TOPIC_UNRESOLVED

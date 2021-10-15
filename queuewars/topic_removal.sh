#!/bin/bash

KAFKA_HOME="kafka"
ZK="--zookeeper localhost:2181"

TOPIC_CHUNKS=chunks
TOPIC_CONFIRMED=confirmed
TOPIC_UNRESOLVED=unresolved

$KAFKA_HOME/bin/kafka-topics.sh $ZK --delete --topic $TOPIC_CHUNKS
$KAFKA_HOME/bin/kafka-topics.sh $ZK --delete --topic $TOPIC_CONFIRMED
$KAFKA_HOME/bin/kafka-topics.sh $ZK --delete --topic $TOPIC_UNRESOLVED

import sys

import config
import serde

from config import broker_endpoints
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from multiprocessing import Process
from partitioner import BlockPartitioner
from synchronized import SynchronizedSet
from threading import Thread

def main():
    if len(sys.argv) <= 1:
        partitions = range(config.NUM_PARTITIONS)
    else:
        partitions = map(lambda arg: int(arg),
            filter(lambda arg: arg.isdigit() and int(arg) < config.NUM_PARTITIONS,
                sys.argv[1: min(len(sys.argv), config.NUM_PARTITIONS+1)]))
    
    subprocesses = []
    for part in partitions:
        proc = Process(target=launch_unresolved_filter, args=(part,))
        subprocesses.append(proc)
        proc.start()

def launch_unresolved_filter(partition):
    confirmed_blocks = SynchronizedSet()
    thread_consumer_chunks = Thread(target=consume_chunks, args=(partition, confirmed_blocks))
    thread_consumer_confirmed_blocks = Thread(target=consume_confirmed_blocks, args=(partition, confirmed_blocks))
    thread_consumer_chunks.start()
    thread_consumer_confirmed_blocks.start()

def consume_chunks(partition, confirmed_blocks_shared_set):
    producer_unresolved_chunks = KafkaProducer(
        bootstrap_servers = broker_endpoints(),
        key_serializer = serde.unsigned_integer_serialize,
        value_serializer = serde.object_serialize)

    consumer_chunks = KafkaConsumer(
        bootstrap_servers = broker_endpoints(),
        group_id = "unresolved-router-%d" % partition,
        key_deserializer = serde.unsigned_integer_deserialize,
        value_deserializer = serde.object_deserialize,
        enable_auto_commit = True,
        auto_offset_reset = 'earliest')
    consumer_chunks.assign([TopicPartition("chunks", partition)])

    for message in consumer_chunks:
        if message.key not in confirmed_blocks_shared_set:
            chunk = { field: message.value[field] for field in ["id", "weight"] }
            chunk["parent"] = message.key
            producer_unresolved_chunks.send("unresolved",
                key=message.key, value=chunk, partition=partition)

def consume_confirmed_blocks(partition, confirmed_blocks_shared_set):
    consumer_confirmed = KafkaConsumer(
        bootstrap_servers = broker_endpoints(),
        group_id = "unresolved-rou-ter-%d" % partition,
        key_deserializer = serde.unsigned_integer_deserialize,
        value_deserializer = serde.string_deserialize,
        enable_auto_commit = True,
        auto_offset_reset = 'earliest')
    consumer_confirmed.assign([TopicPartition("confirmed", partition)])

    for message in consumer_confirmed:
        confirmed_blocks_shared_set.add(message.key)

if __name__ == '__main__':
    main()

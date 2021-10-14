import sys

import api
import config
import serde

from config import broker_endpoints
from kafka import KafkaConsumer, TopicPartition
from multiprocessing import Process

def main():
    if len(sys.argv) <= 1:
        partitions = range(config.NUM_PARTITIONS)
    else:
        partitions = map(lambda arg: int(arg),
            filter(lambda arg: arg.isdigit() and int(arg) < config.NUM_PARTITIONS,
                sys.argv[1 : min(len(sys.argv), config.NUM_PARTITIONS+1)]))
    
    subprocesses = []
    for part in partitions:
        proc = Process(target=submit_block_chunks, args=(part,))
        subprocesses.append(proc)
        proc.start()

def submit_block_chunks(partition):
    consumer = KafkaConsumer(
        bootstrap_servers = broker_endpoints(),
        group_id="block-submitter-%d" % partition,
        key_deserializer = serde.unsigned_integer_deserialize,
        value_deserializer = serde.object_deserialize,
        enable_auto_commit = True,
        auto_offset_reset = 'earliest')
    consumer.assign([TopicPartition("unresolved", partition)])

    chunks_processed_by_block = {}
    for message in consumer:
        process_chunk(chunks_processed_by_block, message.key, message.value)

def process_chunk(blocks, block_id, chunk):
    if block_id not in blocks:
        blocks[block_id] = { "weight": 0, "chunks": [] }
    b = blocks[block_id]
    b["weight"] += chunk["weight"]
    b["chunks"].append(chunk["id"])
    if b["weight"] >= 1.:
        api.confirm(block_id, b["chunks"])

if __name__ == '__main__':
    main()

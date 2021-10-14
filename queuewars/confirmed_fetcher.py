import signal
import sys
import threading
import time

import api
import config
import serde

from config import broker_endpoints
from kafka import KafkaProducer
from partitioner import BlockPartitioner

confirmed_local = set()

def main():
    producer = KafkaProducer(
        bootstrap_servers = broker_endpoints(),
        key_serializer = serde.unsigned_integer_serialize,
        value_serializer = serde.string_serialize,
        partitioner = BlockPartitioner(config.NUM_BLOCKS))

    while True:
        confirmed_server = api.fetch_confirmed()
        for bk in confirmed_server:
            b = int(bk)
            if b not in confirmed_local:
                producer.send("confirmed", key=b, value=confirmed_server[bk])
                confirmed_local.add(b)
        time.sleep(5)

def sigint_handler(signum, frame):
    print("%d blocks were confirmed" % len(confirmed_local))
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    main()

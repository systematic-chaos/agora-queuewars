import api
import config
import serde

from config import broker_endpoints
from kafka import KafkaProducer
from partitioner import BlockPartitioner

def main():
    producer = KafkaProducer(
        bootstrap_servers = broker_endpoints(),
        key_serializer = serde.unsigned_integer_serialize,
        value_serializer = serde.object_serialize,
        partitioner = BlockPartitioner(config.NUM_BLOCKS))
    
    n_chunks = 0
    chunks = api.fetch()
    
    for chunk in chunks:
        producer.send("chunks", key=chunk["parent"], value=chunk)
        n_chunks += 1
    
    print("%d chunks transmitted" % n_chunks)

if __name__ == '__main__':
    main()

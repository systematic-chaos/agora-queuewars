import json
import signal
import sys

from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic

# 1. CREATE TOPIC
# bin/kafka-topics.sh --zookeeper localhost:2181 --create --replication-factor 1 --partitions 1 --topic monkeys
admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092', client_id="test")
admin_client.create_topics(new_topics=[NewTopic(name="monkeys", num_partitions=1, replication_factor=1)])

def sigint_handler(signum, frame):
    admin_client.delete_topics(topics=["monkeys"])
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

# 2. PRODUCER
# In this demo, we push two messages to topic named "monkeys"
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
print("Publishing two messages...")
producer = KafkaProducer(bootstrap_servers='localhost:9092')
message1 = json.dumps({ "foo": 1, "bar": "penguin" }).encode('utf-8')
message2 = json.dumps({ "hello": 1, "world": "bar" }).encode('utf-8')
producer.send("monkeys", message1)
producer.send("monkeys", message2)

# 3. CONSUMER
# Reads continuously messages from "monkeys" topic
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
print("Subscribing to topic and reading messages... (CTRL-C to terminate)")
consumer = KafkaConsumer('monkeys',
    #auto_offset_reset='latest',
    group_id="work-queue",
    enable_auto_commit=False,
    auto_offset_reset='earliest',
    value_deserializer = lambda m: json.loads(m.decode('utf-8')),
    bootstrap_servers=['localhost:9092'])

for message in consumer:
    print("RECEIVED", message)

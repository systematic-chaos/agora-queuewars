import json
import api
import math

from kafka import KafkaProducer

# PRODUCER
# Goals: read N chunks, publish them on queue
# Decide:
# - 1 or N topics
# - 1 or N partitions per topic
# - Consumer groups?

def main():
    #producer = KafkaProducer(bootstrap_servers='localhost:9092')
    chunks = api.fetch()
    for chunk in chunks:
        try:
            print("Parent {}\tchunk {}".format(chunk["parent"], chunk))
        except Exception as e:
            print(e.message)

if __name__ == '__main__':
    main()

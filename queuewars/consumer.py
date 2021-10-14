import api
import sys
import json

from kafka import KafkaConsumer

# CONSUMER
# Goals: read from queue, confirm when sum = 1
# Decide:
# - 1 or N topics
# - 1 or N partitions per topic
# - Consumer groups?

def main():
    # TODO Check sum equals 1, then send the whole block
    # Each block might have variable number of chunks
    # To confirm block, use api.confirm
    topic = 'fu-' + sys.argv[1]
    blocks = {}

if __name__ == '__main__':
    main()

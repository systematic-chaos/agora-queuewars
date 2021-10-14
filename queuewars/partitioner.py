import math
import sys

from kafka.partitioner.base import Partitioner
from serde import unsigned_integer_deserialize

class BlockPartitioner(Partitioner):

    def __init__(self, num_blocks, num_partitions=1):
        self.num_blocks = num_blocks
        self.num_partitions = num_partitions
    
    def __call__(self, key, all_partitions, available_partitions=None):
        partitions = available_partitions if available_partitions else all_partitions
        self.num_partitions = len(partitions)
        page_size = self.num_blocks / self.num_partitions
        key = unsigned_integer_deserialize(key)
        return partitions[math.floor(key / page_size)]

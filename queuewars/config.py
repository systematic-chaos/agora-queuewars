OWNER = 'four'   # one, two, three, four, five, six
BASE_URL = "http://localhost:9000"

BASE_PORT = 9092
NUM_BROKERS = 2
NUM_PARTITIONS = 16
NUM_BLOCKS = 1600

def broker_endpoints():
    return [ 'localhost:' + str(p) for p in range(BASE_PORT, BASE_PORT+NUM_BROKERS) ]

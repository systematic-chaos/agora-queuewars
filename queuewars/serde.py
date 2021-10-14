import json
import sys

def string_serialize(string):
    return string.encode('utf-8')

def string_deserialize(str_bytes):
    return str_bytes.decode('utf-8')

def object_serialize(obj):
    return string_serialize(json.dumps(obj))

def object_deserialize(obj_bytes):
    return json.loads(string_deserialize(obj_bytes))

def unsigned_integer_serialize(uint):
    return uint.to_bytes(len(str(uint)), byteorder=sys.byteorder)

def unsigned_integer_deserialize(uint_bytes):
    return int.from_bytes(uint_bytes, byteorder=sys.byteorder)

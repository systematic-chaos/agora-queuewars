from collections import namedtuple

Chunk = namedtuple('Chunk', ['id', 'parent', 'weight'])

ConfirmedBlock = namedtuple('ConfirmedBlock', ['id', 'owner'])

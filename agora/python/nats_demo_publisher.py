import asyncio
import signal

from datetime import datetime

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

def run(loop):
  nc = NATS()
  yield from nc.connect(servers=["nats://127.0.0.1:4222"], io_loop=loop)

  yield from nc.publish("foo.thing", b'Hello!')
  message = 'Current data: at {now}'.format(now=datetime.now().isoformat())
  yield from nc.publish("foo.thing", message.encode())

  yield from nc.flush()
  yield from nc.close()

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run(loop))
  loop.close()

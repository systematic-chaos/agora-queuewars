const NATS = require('nats');
const nats = NATS.connect({ servers: ['nats://127.0.0.1:4222'] });

nats.subscribe('foo.*', (msg, reply, subject) => {
  console.log({ msg, reply, subject });
});

nats.subscribe('foo.*.thing', (msg, reply, subject) => {
  console.log({ msg, reply, subject });
});

nats.subscribe('prices.daily', { queue: 'work01' }, (msg, reply, subject) => {
  console.log({ msg, reply, subject });
});

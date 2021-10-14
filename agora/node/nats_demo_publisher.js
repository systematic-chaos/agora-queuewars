const NATS = require('nats');
const nats = NATS.connect({ servers: ['nats://127.0.0.1:4222'] });

nats.publish('foo.bar', `FIRST ${new Date().toISOString()}`, () => {
  nats.publish('foo.yeah.thing', `SECOND ${new Date().toISOString()}`, () => {
    nats.close();
  });
});

// const { random } = require('./random');
// nats.publish('prices.daily', JSON.stringify({ MSFT: random(0, 100) }), () => {
//   nats.close();
// });

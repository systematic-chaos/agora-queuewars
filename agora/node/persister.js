const { simulateDatabase } = require('./simulate');
const NATS = require('nats');

const persisterId = process.argv.length > 2 ? process.argv.slice(-1)[0] : random(1, 9);
const persistenceQueue = 'mbda.persistence';

const db = simulateDatabase(persisterId);

var nats = NATS.connect();

// Persister should get messages from queue and store them using `db.save` method
// After that, it should send back an ACK confirmation for that message.
var topic = nats.subscribe(persistenceQueue, { queue: 'persistence' }, function(msg) {
  message = JSON.parse(msg);
  db.save(message).then(ack => {
    // Store received message in the database (simulated!)
    console.log('Message properly stored', ack);
    nats.publish(message.shard + '.ack', JSON.stringify(ack));
  });
});

function exit() {
  nats.unsubscribe(topic);
  nats.close();
  process.exit();
}

process.on('SIGINT', exit);
process.on('SIGTERM', exit);

const { shards, simulateClients } = require('./simulate');
const { pick } = require('./random');
const NATS = require('nats');
const persistenceQueue = 'mbda.persistence';

const shardId = process.argv.slice(-1)[0];
if (!shards.some(s => s === shardId)) {
  console.error('ERROR'.red, 'Unknown shardId, available:', shards.join('.'));
  console.error('Usage: node gateway.js <[A-D]>');
  process.exit(-1);
}

console.log('START'.bgCyan.white.bold, 'shardId:', shardId);

nats = NATS.connect();

var peers = shards.filter(item => item != shardId);

function onSend(msg) {
  nats.publish(pick(peers), msg);
}

function onReceive(msg) {
  console.debug(`Message ${msg.id} from user ${msg.user}, connected to shard ${msg.shard}.`);
  let ackR = { messageId: msg.id, persisterId: shardId };
  nats.publish(msg.shard + '.ack', JSON.stringify(ackR));
  nats.publish(persistenceQueue, JSON.stringify(msg));
}

const websocket = simulateClients(shardId, { sendFn: onSend, receiveFn: onReceive });

// My input messages queue
nats.subscribe(shardId, websocket.receive);

// My input ACKs queue
// This implementation consumes ACKs but does not process them
nats.subscribe(shardId + '.ack', websocket.ack);

function exit() {
  nats.unsubscribe(shardId);
  nats.unsubscribe(shardId + '.ack');
  nats.close();
  process.exit();
}

process.on('SIGINT', exit);
process.on('SIGTERM', exit);

setInterval(() => {
  let message = websocket.generate();
  websocket.send(message);
}, 1000);

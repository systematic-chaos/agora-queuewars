const colors = require('colors');

const { identifier, name, sentence, random, pick } = require('./random');

const shards = ['A', 'B', 'C', 'D'];

const simulateClients = (shardId, callbacks) => ({
  send: message => {
    console.log('SND'.cyan, message.id);
    var sendFn = callbacks.sendFn;
    if (typeof sendFn !== 'undefined') sendFn(JSON.stringify(message));
  },

  ack: ackr => {
    ackr = JSON.parse(ackr);
    if (isNaN(ackr.persisterId)) {
      // Primer ACK, procedente de nodo gemelo
      console.log('ACK RECEIVED'.yellow, ackr.messageId, `[${ackr.persisterId}]`.dim.green);
    } else {
      // Segundo ACK, procedente del persister
      console.log('ACK PERSISTED'.green, ackr.messageId, `[${ackr.persisterId}]`.dim.green, `${ackr.time}ms`);
    }
    var ackFn = callbacks.ackFn;
    if (typeof ackFn !== 'undefined') ackFn(ackr);
  },

  generate: () => {
    const shard = pick(shards);
    const message = {
      id: identifier(shard),
      shard: shardId,
      user: name(),
      text: sentence()
    };
    return message;
  },
  receive: message => {
    console.log('RCV', message);
    var receiveFn = callbacks.receiveFn;
    if (typeof receiveFn !== 'undefined') receiveFn(JSON.parse(message));
  }
});

const simulateDatabase = persisterId => {
  console.log('PERSISTER'.bgRed.white.bold, persisterId);
  return {
    save: ({ id }) => {
      console.log(`SAVE [${persisterId}]`.grey, id.grey);
      return new Promise((resolve, reject) => {
        const delayInMs = random(10, 1000);
        setTimeout(() => {
          const ack = {
            messageId: id,
            persisterId,
            time: delayInMs
          };
          console.log(`SAVE [${persisterId}]`.green, id, `(${delayInMs}ms)`);
          resolve(ack);
        }, delayInMs);
      });
    }
  };
};

module.exports = { simulateClients, simulateDatabase, shards };

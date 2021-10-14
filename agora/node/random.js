const crypto = require('crypto');
const data = require('./data.json');

const random = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);
const pick = items => items[random(0, Math.max(items.length - 1, 0))];

const identifier = prefix => {
  const rn = crypto.randomFillSync(new Uint8Array(4));
  return `${prefix}${rn[0].toString('16').toUpperCase()}`;
};

const name = () => pick(data.people);
const sentence = () => pick(data.sentences);

module.exports = { pick, random, name, sentence, identifier };

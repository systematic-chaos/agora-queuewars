# Agora

This belongs to a workshop based on queues and NATS.io. It showcases basic usage of NATS queues and also a case study on a chat application.

## How to run it

1.  Start NATS in docker container:

```
docker run -p 4222:4222 -p 8222:8222 -p 6222:6222 --name gnatsd -ti nats:latest
```

2.  Install dependencies

```
cd node
npm install
```

3.  Open two new terminals, start `gateway` and `persister` processes:

```
node gateway.js A
node gateway.js B
```

```
node persister.js 1
node persister.js 2
node persister.js 3
```

## NATS 101

### Setup

Download NATS from http://nats.io, unpack it and run:

```
./gnatsd -m 8222
```

It enables two ports, `4222` for the procotol and `8222` with some small information site.

It can also be run via docker:

```
docker run -p 4222:4222 -p 8222:8222 -p 6222:6222 --name gnatsd -ti nats:latest
```

### Protocol basics

Open two terminals, and telnet to port `4222`.

```
$ telnet localhost 4222
```

Then you can subscribe to messages sent to `foo.*`:

```
sub foo.* 90
```

Then try publishing some message from second terminal:

```
pub foo.bar 5
hello
```

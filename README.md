# <img src="resource/logo.png" width=80 /> pytxhorn

__WARNING__: *pytxhorn is still developing, so please be patient if things change or features iterate and change quickly. Once pytxhorn hits 1.0, it will slow down considerably!*

pytxhorn is a standalone, easy-to-use Python module implementing the full Bitcoin SPV client protocol.

It's designed with mobile Lightning Network clients and compatible with [lnd](https://github.com/lightningnetwork/lnd);

Now you must run a full bitcoin node to serve Lightning Network, pytxhorn wants to provide a simple and light node for lightning network in the future;

Pytxhorn is inspired with [pyspv](https://github.com/sarchar/pyspv), [python-bitconlib](https://github.com/petertodd/python-bitcoinlib), [btcpy](https://github.com/chainside/btcpy), [neutrino](https://github.com/lightninglabs/neutrino);

## Requirements

```
pip install -r requirements.txt
```


## Roadmap to v1 && Features

* [TODO] SPV implementation, so relatively lightweight
* [TODO] Python, useful for server and user applications
* [TODO] Testnet support
* [TODO] Extensible payment monitor and transaction building system
* [TODO] simple mini api set compatible with [bitcore core rpc](https://bitcoincore.org/en/doc/0.18.0/)

## Commands

Available commands:

* /peers - returns running bitcoin nodes
* /broadcast - force broadcast tx to all nodes

## Documentation

#### TODO

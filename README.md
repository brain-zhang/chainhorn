# <img src="resource/logo.png" width=80 /> chainhorn

__WARNING__: *chainhorn is still developing, so please be patient if things change or features iterate and change quickly. Once chainhorn hits 1.0, it will slow down considerably!*

chainhorn is a standalone, easy-to-use Python module implementing the full Bitcoin SPV client protocol.

It's designed with mobile Lightning Network clients and compatible with [lnd](https://github.com/lightningnetwork/lnd);

Now you must run a full bitcoin node to serve Lightning Network, chainhorn wants to provide a simple and light node for lightning network in the future;

Chainhorn is inspired with [pyspv](https://github.com/sarchar/pyspv), [python-bitconlib](https://github.com/petertodd/python-bitcoinlib), [btcpy](https://github.com/chainside/btcpy), [neutrino](https://github.com/lightninglabs/neutrino), [pycoind](https://github.com/ricmoo/pycoind);

## Requirements

```
pip install -r requirements.txt
apt install supervisor
```

## Run

```
bin/chainhorn start
```


## Roadmap to v1 && Features

* [TODO] SPV implementation, so relatively lightweight
* [TODO] Python, useful for server and user applications
* [TODO] Testnet support
* [TODO] Extensible payment monitor and transaction building system
* [TODO] Support for segwit
* [TODO] Support for [BIP157](https://github.com/bitcoin/bips/blob/master/bip-0157.mediawiki)
* [TODO] Support for [BIP158](https://github.com/bitcoin/bips/blob/master/bip-0158.mediawiki)
* [TODO] simple mini api set compatible with [bitcore core rpc](https://bitcoincore.org/en/doc/0.18.0/)


## Commands

Available commands:

* GET   '/v1/node'
* GET   '/v1/node/peers'
* PUT   '/v1/node/shutdown'
* PUT   '/v1/node/start'
* GET   '/v1/wallet'
* POST  '/v1/wallet/address'
* POST  '/v1/wallet/spends'
* POST  '/v1/wallet/sendtoaddress'
* POST  '/v1/wallet/importprivkey/<string:wif>'
* GET   '/v1/wallet/dumpprivkey/<string:address>'
* POST  '/v1/wallet/broadcasttx/<string:tx>'

## Documentation

#### TODO

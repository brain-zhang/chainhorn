# -*- coding: utf-8 -*-

import logging
import sys

from .node import get_spv_node
from .wallet import (getinfo,
                     getnewaddress,
                     sendrawtransaction,
                     listspends,
                     dumpprivkey)

from flask import Flask
from flask import request
from flask_restful import Resource, Api

logger = logging.getLogger('default')

app = Flask(__name__)
api = Api(app)
spv = get_spv_node()
API_VERSION = 'v1'


def url_version_wrapper(url):
    wrapper_url = "/{}{}".format(API_VERSION, url)
    return wrapper_url


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()


def shutdown_handler(signal, frame):
    print('CTRL-C pressed!')
    spv.shutdown()
    sys.exit(0)


class NodeGetAllPeers(Resource):
    def get(self):
        network_manager = spv.get_network_manager()
        peers = network_manager.get_peers()
        return {'peers': list(peers.keys())}, 200


class NodeShutDown(Resource):
    def get(self):
        spv.shutdown()
        return {'shutdown': 'ok'}, 200


class NodeStart(Resource):
    def get(self):
        spv.start()
        return {'start': 'ok'}, 200


class WalletGetInfo(Resource):
    def get(self):
        info = getinfo()
        return {'walletinfo': info}, 200


class WalletBroadcastTx(Resource):
    def post(self, tx):
        sendrawtransaction(tx)
        return {'broadcast': 'ok'}, 200


class WalletGenNewAddress(Resource):
    def post(self):
        new_address = getnewaddress()
        return {'new_address': new_address}, 200


class WalletGetSpends(Resource):
    def get(self):
        spents = listspends()
        return spents, 200


class WalletDumpPrivkey(Resource):
    def get(self, address):
        key = dumpprivkey(address)
        return key, 200


api.add_resource(NodeGetAllPeers, url_version_wrapper('/node/peers'))
api.add_resource(NodeShutDown, url_version_wrapper('/node/shutdown'))
api.add_resource(NodeStart, url_version_wrapper('/node/start'))
api.add_resource(WalletGetInfo, url_version_wrapper('/wallet'))
api.add_resource(WalletGenNewAddress, url_version_wrapper('/wallet/address'))
api.add_resource(WalletGetSpends, url_version_wrapper('/wallet/spends'))
api.add_resource(WalletDumpPrivkey, url_version_wrapper('/wallet/dumpprivkey/<string:address>'))
api.add_resource(WalletBroadcastTx, url_version_wrapper('/wallet/broadcasttx/<string:tx>'))


def get_app():
    logger.info("!!!!!!!!!===========construct restapp============!!!!!!!!!!!!!!!!!!!!!")
    return app

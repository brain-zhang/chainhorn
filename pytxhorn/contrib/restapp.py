# -*- coding: utf-8 -*-

import logging
import sys

from .node import get_spv_node
from .wallet import (getinfo,
                     getnewaddress,
                     sendrawtransaction,
                     listspends,
                     sendtoaddress,
                     sendspendtoaddress,
                     dumpprivkey)

from flask import Flask
from flask import request
from flask_restful import Resource, Api
from flask_restful import reqparse


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


class NodeGetInfo(Resource):
    def get(self):
        info = spv.getinfo()
        return {'nodeinfo': info}, 200


class NodeGetAllPeers(Resource):
    def get(self):
        network_manager = spv.get_network_manager()
        peers = network_manager.get_peers()
        return {'peers': list(peers.keys())}, 200


class NodeShutDown(Resource):
    def put(self):
        spv.shutdown()
        return {'shutdown': 'ok'}, 200


class NodeStart(Resource):
    def put(self):
        spv.start()
        return {'start': 'ok'}, 200


class WalletGetInfo(Resource):
    def get(self):
        info = getinfo(spv)
        return {'walletinfo': info}, 200


class WalletBroadcastTx(Resource):
    def post(self, tx):
        sendrawtransaction(spv, tx)
        return {'broadcast': 'ok'}, 200


class WalletGenNewAddress(Resource):
    def post(self):
        new_address = getnewaddress(spv)
        return {'new_address': new_address}, 200


class WalletGetSpends(Resource):
    def get(self):
        spents = listspends(spv)
        return spents, 200


class WalletSendtoAddress(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', type=str, help='sendto address')
        parser.add_argument('amount', type=str, help='send amount with 1B unit')
        args = parser.parse_args()
        address = args['address']
        amount = args['amount']
        return sendtoaddress(spv, address, amount), 200


class WalletSendSpendtoAddress(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('spendhash', type=str, help='send spend to address')
        parser.add_argument('address', type=str, help='send spend to address')
        parser.add_argument('amount', type=str, help='send amount with 1B unit')
        args = parser.parse_args()
        spendhash = args['spendhash']
        address = args['address']
        amount = args['amount']
        return sendspendtoaddress(spv, spendhash, address, amount), 200


class WalletDumpPrivkey(Resource):
    def get(self, address):
        key = dumpprivkey(address)
        return key, 200


api.add_resource(NodeGetInfo, url_version_wrapper('/node'))
api.add_resource(NodeGetAllPeers, url_version_wrapper('/node/peers'))
api.add_resource(NodeShutDown, url_version_wrapper('/node/shutdown'))
api.add_resource(NodeStart, url_version_wrapper('/node/start'))
api.add_resource(WalletGetInfo, url_version_wrapper('/wallet'))
api.add_resource(WalletGenNewAddress, url_version_wrapper('/wallet/address'))
api.add_resource(WalletGetSpends, url_version_wrapper('/wallet/spends'))
api.add_resource(WalletSendtoAddress, url_version_wrapper('/wallet/sendtoaddress'))
api.add_resource(WalletDumpPrivkey, url_version_wrapper('/wallet/dumpprivkey/<string:address>'))
api.add_resource(WalletBroadcastTx, url_version_wrapper('/wallet/broadcasttx/<string:tx>'))


def get_app():
    logger.info("!!!!!!!!!===========construct restapp============!!!!!!!!!!!!!!!!!!!!!")
    return app

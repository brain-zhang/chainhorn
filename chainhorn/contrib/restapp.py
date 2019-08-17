# -*- coding: utf-8 -*-

import logging
import sys

from .node import get_spv_node
from .walletapp import (getinfo,
                        getnewaddress,
                        sendrawtransaction,
                        listspends,
                        sendtoaddress,
                        sendspendtoaddress,
                        importprivkey,
                        dumpprivkey)

from flask import Flask
from flask import request
from flask_restplus import Api, Resource, reqparse, fields


logger = logging.getLogger('default')

API_VERSION = 'v1'
app = Flask(__name__)
spv = get_spv_node()
api = Api(app, version=API_VERSION, title='Chainhorn API',
          description='Chainhorn API',
)

ns_node = api.namespace('node', description='chainhorn node operations')
ns_wallet = api.namespace('wallet', description='chainhorn wallet operations')


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
    @ns_node.doc('get node info')
    def get(self):
        info = spv.getinfo()
        return {'nodeinfo': info}, 200


class NodeGetAllPeers(Resource):
    @ns_node.doc('get peers list')
    def get(self):
        network_manager = spv.get_network_manager()
        peers = network_manager.get_peers()
        return {'peers': list(peers.keys())}, 200


class NodeShutDown(Resource):
    @ns_node.doc('shutdown node')
    def put(self):
        spv.shutdown()
        return {'shutdown': 'ok'}, 200


class NodeStart(Resource):
    @ns_node.doc('start node')
    def put(self):
        spv.start()
        return {'start': 'ok'}, 200


class WalletGetInfo(Resource):
    @ns_wallet.doc('get wallet info')
    def get(self):
        info = getinfo(spv)
        return {'walletinfo': info}, 200


class WalletBroadcastTx(Resource):
    @ns_wallet.doc('broadcast raw tx')
    @ns_wallet.param('tx', 'The transaction hash identifier')
    def post(self, tx):
        sendrawtransaction(spv, tx)
        return {'broadcast': 'ok'}, 200


class WalletGenNewAddress(Resource):
    @ns_wallet.doc('generate new address')
    def post(self):
        new_address = getnewaddress(spv)
        return {'new_address': new_address}, 201


class WalletGetSpends(Resource):
    @ns_wallet.doc('list unspends')
    def get(self):
        spents = listspends(spv)
        return spents, 200


sendto_address_model = api.model('SendToAddressParams', {
    'address': fields.String(required=True, description='send to address'),
    'amount': fields.String(required=True, description='send amount with 1B unit')
})


class WalletSendtoAddress(Resource):
    @ns_wallet.doc('send amount to specified address')
    @ns_wallet.marshal_with(sendto_address_model, code=200)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', type=str, help='send to address')
        parser.add_argument('amount', type=str, help='send amount with 1B unit')
        args = parser.parse_args()
        address = args['address']
        amount = args['amount']
        return sendtoaddress(spv, address, amount), 200


sendto_spend_address_model = api.model('SendToSpendAddressParams', {
    'spendhash': fields.String(required=True, description='send to address spendhash'),
    'address': fields.String(required=True, description='send spend to address'),
    'amount': fields.String(required=True, description='send amount with 1B unit')
})


class WalletSendSpendtoAddress(Resource):
    @ns_wallet.doc('send amount to specified address from spendhash')
    @ns_wallet.marshal_with(sendto_spend_address_model, code=200)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('spendhash', type=str, help='send to address spendhash')
        parser.add_argument('address', type=str, help='send spend to address')
        parser.add_argument('amount', type=str, help='send amount with 1B unit')
        args = parser.parse_args()
        spendhash = args['spendhash']
        address = args['address']
        amount = args['amount']
        return sendspendtoaddress(spv, spendhash, address, amount), 200


class WalletImportPrivkey(Resource):
    @ns_wallet.doc('import wif private key')
    @ns_wallet.param('wif', 'The wif key')
    def post(self, wif):
        import_address = importprivkey(spv, wif)
        return import_address, 200


class WalletDumpPrivkey(Resource):
    @ns_wallet.doc('dump wif private key by address')
    @ns_wallet.param('address', 'address')
    def get(self, address):
        key = dumpprivkey(spv, address)
        return key, 200


api.add_resource(NodeGetInfo, url_version_wrapper('/node'))
api.add_resource(NodeGetAllPeers, url_version_wrapper('/node/peers'))
api.add_resource(NodeShutDown, url_version_wrapper('/node/shutdown'))
api.add_resource(NodeStart, url_version_wrapper('/node/start'))
api.add_resource(WalletGetInfo, url_version_wrapper('/wallet'))
api.add_resource(WalletGenNewAddress, url_version_wrapper('/wallet/address'))
api.add_resource(WalletGetSpends, url_version_wrapper('/wallet/spends'))
api.add_resource(WalletSendtoAddress, url_version_wrapper('/wallet/sendtoaddress'))
api.add_resource(WalletSendSpendtoAddress, url_version_wrapper('/wallet/sendspendtoaddress'))
api.add_resource(WalletImportPrivkey, url_version_wrapper('/wallet/importprivkey/<string:wif>'))
api.add_resource(WalletDumpPrivkey, url_version_wrapper('/wallet/dumpprivkey/<string:address>'))
api.add_resource(WalletBroadcastTx, url_version_wrapper('/wallet/broadcasttx/<string:tx>'))


def get_app():
    logger.info("!!!!!!!!!===========construct restapp============!!!!!!!!!!!!!!!!!!!!!")
    return app

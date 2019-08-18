# -*- coding: utf-8 -*-

import json
import logging
import sys

from flask_httpauth import HTTPTokenAuth
from flask import Flask
from flask import request
from flask_restplus import Api, Resource, fields

from .node import get_spv_node
from .walletapp import (getinfo,
                        getnewaddress,
                        sendrawtransaction,
                        listspends,
                        sendtoaddress,
                        sendspendtoaddress,
                        importprivkey,
                        dumpprivkey)
from settings import AUTHORIZATIONS, DEFAULT_TOKENS


logger = logging.getLogger('default')
app = Flask(__name__)
spv = get_spv_node()

API_VERSION = 'v1'

api = Api(app,
          version=API_VERSION,
          authorizations=AUTHORIZATIONS,
          security=list(AUTHORIZATIONS.keys()),
          title='Chainhorn API',
          description='Chainhorn API',
)

ns_node = api.namespace('node', path="/{}{}".format(API_VERSION, '/node'),
                        description='chainhorn node operations')
ns_wallet = api.namespace('wallet', path="/{}{}".format(API_VERSION, '/wallet'),
                          description='chainhorn wallet operations')

auth = HTTPTokenAuth()
tokens = DEFAULT_TOKENS


@auth.verify_token
def verify_token(token):
    if request.headers.get('APIKEY', '').strip()==tokens['APIKEY'] and \
       request.headers.get('APPID', '').strip() == tokens['APPID']:
        return True
    else:
        return False


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()


def shutdown_handler(signal, frame):
    print('CTRL-C pressed!')
    spv.shutdown()
    sys.exit(0)


@ns_node.route('')
class NodeGetInfo(Resource):
    @ns_node.doc('get node info')
    @auth.login_required
    def get(self):
        '''get node info'''
        info = spv.getinfo()
        return {'nodeinfo': info}, 200


@ns_node.route('/peers')
class NodeGetAllPeers(Resource):
    @ns_node.doc('get peers list')
    @auth.login_required
    def get(self):
        '''get peers list'''
        network_manager = spv.get_network_manager()
        peers = network_manager.get_peers()
        return {'peers': list(peers.keys())}, 200


@ns_node.route('/shutdown')
class NodeShutDown(Resource):
    @ns_node.doc('shutdown node')
    @auth.login_required
    def put(self):
        '''shutdown node'''
        spv.shutdown()
        return {'shutdown': 'ok'}, 200


@ns_node.route('/start')
class NodeStart(Resource):
    @ns_node.doc('start node')
    @auth.login_required
    def put(self):
        '''start node'''
        spv.start()
        return {'start': 'ok'}, 200


@ns_wallet.route('')
class WalletGetInfo(Resource):
    @ns_wallet.doc('get wallet info')
    @auth.login_required
    def get(self):
        '''get wallet info'''
        info = getinfo(spv)
        return {'walletinfo': info}, 200


@ns_wallet.route('/broadcast/string:tx')
class WalletBroadcastTx(Resource):
    @ns_wallet.doc('broadcast raw tx')
    @ns_wallet.param('tx', 'The transaction hash identifier')
    @auth.login_required
    def post(self, tx):
        '''broadcast raw tx'''
        sendrawtransaction(spv, tx)
        return {'broadcast': 'ok'}, 200


@ns_wallet.route('/address')
class WalletGenNewAddress(Resource):
    @ns_wallet.doc('generate new address')
    @auth.login_required
    def post(self):
        '''generate new address'''
        new_address = getnewaddress(spv)
        return {'new_address': new_address}, 201


@ns_wallet.route('/spends')
class WalletGetSpends(Resource):
    @ns_wallet.doc('list unspends')
    @auth.login_required
    def get(self):
        '''list unspends'''
        spents = listspends(spv)
        return spents, 200


sendto_address_model = api.model('SendToAddressParams', {
    'address': fields.String(required=True, description='send to address'),
    'amount': fields.String(required=True, description='send amount with 1B unit')
})


@ns_wallet.route('/sendtoaddress')
class WalletSendtoAddress(Resource):
    @ns_wallet.doc('send amount to specified address')
    @ns_wallet.expect(sendto_address_model, code=200)
    @auth.login_required
    def post(self):
        '''send amount to specified address, exp:send 0.01btc to 1xxxx'''
        address = api.payload['address']
        amount = str(api.payload['amount'])
        return sendtoaddress(spv, address, amount), 200


sendto_spend_address_model = api.model('SendToSpendAddressParams', {
    'spendhash': fields.String(required=True, description='send to address spendhash'),
    'address': fields.String(required=True, description='send spend to address'),
    'amount': fields.Float(required=True, description='send amount with 1B unit')
})


@ns_wallet.route('/sendspendtoaddress')
class WalletSendSpendtoAddress(Resource):
    @ns_wallet.doc('send amount to specified address from spendhash')
    @ns_wallet.expect(sendto_spend_address_model, code=200)
    @auth.login_required
    def post(self):
        '''send amount to specified address from spendhash'''
        spendhash = api.payload['spendhash']
        address = api.payload['address']
        amount = str(api.payload['amount'])
        return sendspendtoaddress(spv, spendhash, address, amount), 200


@ns_wallet.route('importprivkey/<string:wif>')
class WalletImportPrivkey(Resource):
    @ns_wallet.doc('import wif private key')
    @ns_wallet.param('wif', 'The wif key')
    @auth.login_required
    def post(self, wif):
        '''import wif private key'''
        import_address = importprivkey(spv, wif)
        return import_address, 201


@ns_wallet.route('dumpprivkey/<string:address>')
class WalletDumpPrivkey(Resource):
    @ns_wallet.doc('dump wif private key by address')
    @ns_wallet.param('address', 'address')
    @auth.login_required
    def get(self, address):
        '''dump wif private key by address'''
        key = dumpprivkey(spv, address)
        return key, 200


def get_app():
    logger.info("!!!!!!!!!===========construct restapp============!!!!!!!!!!!!!!!!!!!!!")
    return app

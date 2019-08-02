# -*- coding: utf-8 -*-

import logging
import sys
import settings

from .node import get_spv_node
from .core.util import hexstring_to_bytes
from .core.bitcoin import Bitcoin
from .core.transaction import Transaction

from flask import Flask
from flask import request
from flask_restful import Resource, Api

logger = logging.getLogger('default')

app = Flask(__name__)
api = Api(app)
spv = get_spv_node(settings)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()


def shutdown_handler(signal, frame):
    print('CTRL-C pressed!')
    spv.shutdown()
    sys.exit(0)


class GetAllPeers(Resource):
    def get(self):
        network_manager = spv.get_network_manager()
        peers = network_manager.get_peers()
        return {'peers': list(peers.keys())}


class ShutDown(Resource):
    def get(self):
        spv.shutdown()
        return {'shutdown': 'ok'}


class Start(Resource):
    def get(self):
        spv.start()
        return {'start': 'ok'}


class Broadcast(Resource):
    def get(self, tx):
        data = hexstring_to_bytes(tx, reverse=False)
        txobj, _ = Transaction.unserialize(data, Bitcoin)
        spv.broadcast_transaction(txobj)
        return {'broadcast': 'ok'}


api.add_resource(GetAllPeers, '/peers')
api.add_resource(ShutDown, '/shutdown')
api.add_resource(Start, '/start')
api.add_resource(Broadcast, '/broadcast/<string:tx>')


def get_app():
    logger.info("!!!!!!!!!===========construct restapp============!!!!!!!!!!!!!!!!!!!!!")
    return app

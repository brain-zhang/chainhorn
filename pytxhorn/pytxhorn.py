# -*- coding: utf-8 -*-

import settings
import signal
import sys
import threading

from contrib.core import HornNode
from contrib.core.util import hexstring_to_bytes
from contrib.core.bitcoin import Bitcoin
from contrib.core.transaction import Transaction
from contrib.logging import init_logging
from flask import Flask
from flask import request
from flask_restful import Resource, Api

init_logging()
app = Flask(__name__)
api = Api(app)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()


def shutdown_handler(signal, frame):
    print('CTRL-C pressed!')
    spv.shutdown()
    sys.exit(0)


class HornNodeSingleton(HornNode):
    _instance_lock = threading.Lock()

    def __init__(self, **kwargs):
        super(HornNodeSingleton, self).__init__(**kwargs)

    def __new__(cls, *args, **kwargs):
        if not hasattr(HornNodeSingleton, "_instance"):
            with HornNodeSingleton._instance_lock:
                if not hasattr(HornNodeSingleton, "_instance"):
                    HornNodeSingleton._instance = object.__new__(cls)
        return HornNodeSingleton._instance


spv = HornNodeSingleton(app_name=settings.APPNAME,
                        testnet=settings.TESTNET,
                        peer_goal=settings.BITCOIN_NETWORK_PEER_GOAL,
                        broadcast_peer_goal=settings.BITCOIN_NETWORK_BROADCAST_PEER_GOAL,
                        sync_block_start=settings.SYNC_BLOCK_START,
                        listen=(settings.HOST_IP, settings.HOST_PORT),
                    )


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


if __name__ == '__main__':
    spv.start()
    app.run(debug=True, use_reloader=False, host=settings.WEB_HOST_IP, port=settings.WEB_HOST_PORT)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.pause()

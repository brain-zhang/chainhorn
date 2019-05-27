# -*- coding: utf-8 -*-

import settings
import threading

from contrib.pyspv import pyspv
from contrib.pyspv.util import DEBUG, INFO, WARNING, hexstring_to_bytes
from contrib.pyspv.bitcoin import Bitcoin
from contrib.pyspv.transaction import Transaction
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class PyspvSingleton(pyspv):
    _instance_lock = threading.Lock()

    def __init__(self, **kwargs):
        super(PyspvSingleton, self).__init__(**kwargs)

    def __new__(cls, *args, **kwargs):
        if not hasattr(PyspvSingleton, "_instance"):
            with PyspvSingleton._instance_lock:
                if not hasattr(PyspvSingleton, "_instance"):
                    PyspvSingleton._instance = object.__new__(cls)
        return PyspvSingleton._instance


spv = PyspvSingleton(app_name='pytxhorn',
                     peer_goal=settings.BITCOIN_NETWORK_PEER_GOAL,
                     broadcast_peer_goal=settings.BITCOIN_NETWORK_BROADCAST_PEER_GOAL,
                     listen=(settings.HOST_IP, settings.HOST_PORT),
                     logging_level=WARNING)


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
    app.run(debug=True)

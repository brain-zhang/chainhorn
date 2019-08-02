# -*- coding: utf-8 -*-

import os.path
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
RUNTIME_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ETC_ROOT = os.path.join(RUNTIME_ROOT, 'etc')
ETC_RUNTIME_ROOT = os.path.join(ETC_ROOT, 'runtime')
TMP_ROOT = os.path.join(RUNTIME_ROOT, 'var', 'tmp')
STORE_ROOT = os.path.join(RUNTIME_ROOT, 'var', 'store')
LOG_ROOT = os.path.join(RUNTIME_ROOT, 'var', 'log')
DB_ROOT = os.path.join(RUNTIME_ROOT, 'var', 'db')
RUN_ROOT = os.path.join(RUNTIME_ROOT, 'var', 'run')
IPC_ENDPOINT_ROOT = os.path.join(RUN_ROOT, 'ipc')

sys.path.append(PROJECT_ROOT)
LOGGING_LEVEL = 'INFO'

# pytxhorn node config
APPNAME = 'pytxhorn'

BITCOIN_NETWORK_PEER_GOAL = 100

# BITCOIN_NETWORK_BROADCAST_PEER_GOAL must <= BITCOIN_NETWORK_PEER_GOAL
BITCOIN_NETWORK_BROADCAST_PEER_GOAL = 100

SYNC_BLOCK_START = 0

TESTNET = False

HOST_IP = '0.0.0.0'
HOST_PORT = 8033

WEB_HOST_IP = '0.0.0.0'
WEB_HOST_PORT = 5000


# add your settings before these code if you want to make it in local_settings.py
try:
    from local_settings import *
except ImportError:
    pass


# init logging module
from contrib.logging import init_logging
init_logging()

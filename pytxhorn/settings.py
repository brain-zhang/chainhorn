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

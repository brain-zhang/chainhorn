# -*- coding: utf-8 -*-

import logging
import threading
from contrib.core import HornNode

logger = logging.getLogger('default')


class HornNodeSingleton(HornNode):
    _instance_lock = threading.Lock()

    def __init__(self, **kwargs):
        super(HornNodeSingleton, self).__init__(**kwargs)

    def __new__(cls, *args, **kwargs):
        if not hasattr(HornNodeSingleton, "_instance"):
            with HornNodeSingleton._instance_lock:
                if not hasattr(HornNodeSingleton, "_instance"):
                    HornNodeSingleton._instance = object.__new__(cls)
                    logger.info("!!!!!!!!!===========construct hornnode singleton============!!!!!!!!!!!!!!!!!!!!!")
        return HornNodeSingleton._instance


def get_spv_node(settings):
    spv = HornNodeSingleton(app_name=settings.APPNAME,
                            testnet=settings.TESTNET,
                            peer_goal=settings.BITCOIN_NETWORK_PEER_GOAL,
                            broadcast_peer_goal=settings.BITCOIN_NETWORK_BROADCAST_PEER_GOAL,
                            sync_block_start=settings.SYNC_BLOCK_START,
                            listen=(settings.HOST_IP, settings.HOST_PORT),
                    )
    return spv

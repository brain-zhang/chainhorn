# -*- coding: utf-8 -*-

import logging
import threading
import settings as default_settings

from contrib.core import HornNode

logger = logging.getLogger('default')


class HornNodeSingleton(HornNode):
    __instance_lock = threading.Lock()
    __init_flag = False

    def __init__(self, **kwargs):
        if not self.__init_flag:
            super(HornNodeSingleton, self).__init__(**kwargs)
            HornNodeSingleton.__init_flag = True

    def __new__(cls, *args, **kwargs):
        if not hasattr(HornNodeSingleton, "_instance"):
            with HornNodeSingleton.__instance_lock:
                if not hasattr(HornNodeSingleton, "_instance"):
                    HornNodeSingleton._instance = object.__new__(cls)
                    logger.info("!!!!!!!!!===========construct hornnode singleton============!!!!!!!!!!!!!!!!!!!!!")
        return HornNodeSingleton._instance


def get_spv_node(settings=None, need_load_blocks=True):
    if not settings:
        settings = default_settings

    spv = HornNodeSingleton(app_name=settings.APPNAME,
                            testnet=settings.TESTNET,
                            peer_goal=settings.BITCOIN_NETWORK_PEER_GOAL,
                            broadcast_peer_goal=settings.BITCOIN_NETWORK_BROADCAST_PEER_GOAL,
                            sync_block_start=settings.SYNC_BLOCK_START,
                            need_load_blocks=need_load_blocks,
                            listen=(settings.HOST_IP, settings.HOST_PORT),
                    )
    return spv

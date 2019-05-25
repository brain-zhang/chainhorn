# -*- coding: utf-8 -*-

import settings
import time
from contrib import pyspv

if __name__ == '__main__':
    spv = pyspv.pyspv("pytxhorn", peer_goal=100)
    print("pytxhorn start ~~")

    while True:
        network_manager = spv.get_network_manager()
        peers = network_manager.get_peers()
        print('=======================')
        for peer_address in list(peers.keys()):
            print(peer_address)

        time.sleep(30)

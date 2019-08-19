# -*- coding: utf-8 -*-

import unittest
from .models import TestCase
from contrib.core import HornNode
from settings import SKIP_NDBM_TEST


class BlockChainTestCase(TestCase):

    def setUp(self):
        # loading fixtures spv fake node data
        super(BlockChainTestCase, self).setUp()

        spv = HornNode(app_name='chainhorn',
                       testnet=False,
                       peer_goal=10,
                       broadcast_peer_goal=10,
                       sync_block_start=0,
                       listen=('127.0.0.1', 5000),
                       app_datapath=self.temp_fixture_path,
                )
        self.blockchain = spv.blockchain

    @unittest.skipIf(SKIP_NDBM_TEST, "skip dbm test")
    def test_load_blockchain_db(self):
        # loading fixtures spv fake node data

        self.assertEqual(self.blockchain.get_best_chain_height(), 2000)
        best_chain_locator = self.blockchain.get_best_chain_locator()

        locator_hashes = [
            '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
            '0000000069ed32a4d4ad130aa267687f78b25236c5efd1d54abf65a7ee1fa0c0',
            '0000000000a4d1bff90f29495e4c45d96609dcdc278264511d90e5f1602034d5',
            '000000007f6d461815d7d53620358498e179e846a66084f2f6239c5e7a3ae9f6',
            '00000000cabdfa62f62553973d5ba3a0e74eb5b4d6e03366f79bd05f2a7c5646',
            '00000000b47e11bcd166f6da173d0af55ba9164f5d9020fd98278830319793d7',
            '00000000acdfcd699a667d7089a912e5fe83d7cf9e465512b8491f51452e5308',
            '00000000f0655b679fba1aa2d32c0885546e7183667a48a3a1328222d656881e',
            '00000000c7b984d0429b8e9ffa044a776932944d3761eedee5d8b7bedb7a1eb7',
            '000000002ace74c47a24e92806aeefb968258359c2988f1bfd134f4bae233be6',
            '000000002a90502d96e8baa75b749b2fb4fa6491e115314bf7674f1e26ff726e',
            '000000007e95b1d5a9603874ddbae14c6eacf7dcf86429efb91947ea27ca402e',
            '00000000bfebb625430b6483c7f19d2886d1970cda683971fcccca292cc9b7f6',
            '00000000a2c8ede8616565cf6900e5bea3b4f29734b88c31c06462b6327f87b3',
            '00000000379bf01707cf13f4e35dd30493b254508937f7d6b4fcb35948b9afbc',
            '00000000f0876346d33d67c16544d3fe99d6898ad114c59f78dfd8c5f41611b9',
            '000000000f84cb6d276c94f0d8b9ad3d398c164d9eda53491a1102cd4d16ef0d',
            '0000000062436dec026b8c8fcf9aea8554312de16d35888f05d2b41710850477',
            '00000000a1496d802a4a4074590ec34074b76a8ea6b81c1c9ad4192d3c2ea226',
            '00000000dfd5d65c9d8561b4b8f60a63018fe3933ecb131fb37f905f87da951a',
        ]
        self.assertListEqual(locator_hashes, best_chain_locator.get_hashes())

    def tearDown(self):
        super(BlockChainTestCase, self).tearDown()

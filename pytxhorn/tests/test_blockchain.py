# -*- coding: utf-8 -*-

from .models import TestCase
from contrib.pyspv import pyspv


class BlockChainTestCase(TestCase):

    def setUp(self):

        # loading fixtures spv fake node data
        super(BlockChainTestCase, self).setUp()

    def test_load_blockchain_db(self):
        # loading fixtures spv fake node data
        spv = pyspv(app_name='pytxhorn',
                    testnet=False,
                    peer_goal=10,
                    broadcast_peer_goal=10,
                    sync_block_start=0,
                    listen=('127.0.0.1', 5000),
                    app_datapath=self.fixture_path,
                )
        self.blockchain = spv.blockchain
        self.assertEqual(self.blockchain.get_best_chain_height(), 2000)

    def tearDown(self):
        super(TestCase, self).tearDown()

# -*- coding: utf-8 -*-

from .models import TestCase
from contrib.core import HornNode
from contrib.core.keys import PrivateKey


class WalletTestCase(TestCase):

    def setUp(self):
        # loading fixtures spv fake node data
        super(WalletTestCase, self).setUp()

        self.spv = HornNode(app_name='pytxhorn',
                            testnet=False,
                            peer_goal=10,
                            broadcast_peer_goal=10,
                            sync_block_start=0,
                            listen=('127.0.0.1', 5000),
                            app_datapath=self.fixture_path,
                )

    def test_gen_new_address(self):
        # loading fixtures spv fake node data
        pk = PrivateKey.create_new()
        self.spv.wallet.add('private_key', pk, {'label': ''})
        pubkey = pk.get_public_key(compressed=True).as_address(self.spv.coin)
        self.logger.info(pubkey)

    def tearDown(self):
        super(TestCase, self).tearDown()

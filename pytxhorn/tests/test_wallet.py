# -*- coding: utf-8 -*-

from .models import TestCase
from contrib.core import HornNode
from contrib.core.keys import PrivateKey


class WalletTestCase(TestCase):

    def setUp(self):
        # loading fixtures spv fake node data
        super(WalletTestCase, self).setUp()

        self.spv = HornNode(app_name='pytxhorn',
                            testnet=True,
                            peer_goal=10,
                            broadcast_peer_goal=10,
                            sync_block_start=0,
                            listen=('127.0.0.1', 15000),
                            app_datapath=self.temp_fixture_path,
                )

    def test_gen_new_address(self):
        # loading fixtures spv fake node data
        pk = PrivateKey.create_new()
        self.spv.wallet.add('private_key', pk, {'label': ''})
        address = pk.get_public_key(compressed=True).as_address(self.spv.coin)
        self.logger.info(address)

        # test wallet.add_temp
        temp_address_metadata = self.spv.wallet.get_temp('address', address)
        self.logger.info(temp_address_metadata)

        # test wallet.add
        private_key_metadata = self.spv.wallet.get('private_key', pk)
        self.logger.info(private_key_metadata)

    def tearDown(self):
        super(WalletTestCase, self).tearDown()

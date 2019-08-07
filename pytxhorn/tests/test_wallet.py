from .models import TestCase
from contrib.core import HornNode
from contrib.core.keys import PrivateKey
from contrib.wallet import sendspendtoaddress


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

    def test_get_temp_collections(self):
        addresses = [
            'mgSFbgRuX9j1DpDUs2drfvoLd8mUC3G84V',
            'min4h6ixUBnqDvujUzegc1idZ4nyTwBQfB',
            'mjxfYJ8uEKfQgRbd1KHgbWudRpo7G9h4A6',
            'miw2LrQCnm66AiRZ3M45LJt5yZjaxZUGRY',
            'mm2pTcMUStmM4Wj4DgZTggjAPo8zXS7W1v',
            'muuaFueV5DhosVrEViH2B6h6XjLgHWkwZt',
            'n1eKKyX1oY1jEtPvPamcSVHXGGPpkDFXu4',
            'n1xhAbKKxTGTMMGFUqPqnwDFjSYgdKFPKv'
        ]

        collections = self.spv.wallet.get_temp_collections()
        wallet_address = list(collections['address'].keys())
        for address in addresses:
            self.assertIn(address, wallet_address)

    def test_spend_sent(self):
        spendhash = '33e075e7b5099d57550a74e3300aa7586f59d96007e4b847a178beaf8ec40da4'
        address = '2NGZrVvZG92qGYqzTLjCAewvPZ7JE8S8VxE'
        amount = '0.0009'
        result = sendspendtoaddress(self.spv, spendhash, address, amount)
        self.logger.info(result)

    def tearDown(self):
        super(WalletTestCase, self).tearDown()

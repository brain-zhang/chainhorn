from .models import TestCase
from contrib.core import HornNode
from contrib.core.keys import PrivateKey
from contrib.walletapp import sendspendtoaddress
from contrib.core.util import bytes_to_hexstring


class WalletTestnetTestCase(TestCase):

    def setUp(self):
        # loading fixtures spv fake node data
        super(WalletTestnetTestCase, self).setUp()

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
        self.logger.info(pk.as_wif(self.spv.coin, True))

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
        super(WalletTestnetTestCase, self).tearDown()


class WalletMainNetTestCase(TestCase):

    def setUp(self):
        # loading fixtures spv fake node data
        super(WalletMainNetTestCase, self).setUp()

        self.spv = HornNode(app_name='pytxhorn',
                            testnet=False,
                            peer_goal=10,
                            broadcast_peer_goal=10,
                            sync_block_start=0,
                            listen=('127.0.0.1', 15000),
                            app_datapath=self.temp_fixture_path,
                )

    def test_import_wif(self):
        # loading fixtures spv fake node data
        wif = 'KwLfcF1w7X9Hi79viRJJzAc5iqFhxGwPW73bwjGQ5HZ1VZb5SPst'
        pk = PrivateKey.import_wif(wif)
        self.spv.wallet.add('private_key', pk, {'label': ''})
        address = pk.get_public_key(compressed=True).as_address(self.spv.coin)
        self.assertEqual(address, '1875pogmBxMzeYFxt3s9QED8xDGXnc71W3')
        self.assertEqual(bytes_to_hexstring(pk.secret, reverse=False),
                         '039405f36260764a8fabab122a802244580769cc88c8a2b6ff3b5af63b99a960')

    def test_import_wif2(self):
        # loading fixtures spv fake node data
        wif = '5JhayTrDhzDHqCg2v16Y2gZWi4kWF6BFoZR3MyaaxWtyKHzKJ8d'
        pk = PrivateKey.import_wif(wif)
        self.spv.wallet.add('private_key', pk, {'label': ''})
        address = pk.get_public_key(compressed=False).as_address(self.spv.coin)
        self.assertEqual(bytes_to_hexstring(pk.secret, reverse=False),
                         '747b8e8f5bc72bfd91471b61bea30a5d2c798805ed84034584dae2d3e920e11a')
        self.assertEqual(address, '11121ioKu4MCB1LLzPF98AVtzFsEg7UYKm')

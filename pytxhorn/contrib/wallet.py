# -*- coding: utf-8 -*-

import logging

from . import core as horncore
from .utils import exception_printer
from .core import base58
from .core.keys import PrivateKey, PublicKey
from .core.payments.stealth import StealthAddressPayment
from .core.payments.pubkey import PubKeyPayment, PubKeyChange
from .core.payments.multisig import MultisigScriptHashPayment
from .core.script import Script
from .core.script import OP_CHECKMULTISIG
from .core.transaction import Transaction
from .core.util import hexstring_to_bytes, bytes_to_hexstring, base58_check
from .core.wallet import DuplicateWalletItem

logger = logging.getLogger('default')


@exception_printer
def getinfo(spv):
    addresses = spv.wallet.get_temp_collections().get('address', {})
    addresses = list(addresses.keys())
    return {
        'balance': spv.coin.format_money(sum(v for v in spv.wallet.balance.values())),
        'coin': spv.coin.__name__,
        'address': addresses
    }


def get_output_producer(spv, address, amount):
    # Determine the payment type based on the version byte of the address provided
    # (I don't think this is the proper long term solution to different payment types...)
    try:
        address_bytes = int.to_bytes(base58.decode(address),
                                     spv.coin.ADDRESS_BYTE_LENGTH, 'big')
    except OverflowError:
        address_bytes = b''

    k = len(spv.coin.ADDRESS_VERSION_BYTES)
    if address_bytes[:k] == spv.coin.ADDRESS_VERSION_BYTES:
        return PubKeyPayment(address, amount)
    else:
        try:
            address_bytes = int.to_bytes(base58.decode(address),
                                         spv.coin.P2SH_ADDRESS_BYTE_LENGTH, 'big')
        except OverflowError:
            address_bytes = b''

        k = len(spv.coin.P2SH_ADDRESS_VERSION_BYTES)
        if address_bytes[:k] == spv.coin.P2SH_ADDRESS_VERSION_BYTES:
            return MultisigScriptHashPayment(address, amount)
        else:
            try:
                # Drop last 4 bytes because of the checksum
                address_bytes = int.to_bytes(base58.decode(address),
                                             spv.coin.STEALTH_ADDRESS_BYTE_LENGTH, 'big')[:-4]
            except OverflowError:
                address_bytes = b''

            k = len(spv.coin.STEALTH_ADDRESS_VERSION_BYTES)
            j = len(spv.coin.STEALTH_ADDRESS_SUFFIX_BYTES)
            if address_bytes[:k] == spv.coin.STEALTH_ADDRESS_VERSION_BYTES and \
               address_bytes[-j:] == spv.coin.STEALTH_ADDRESS_SUFFIX_BYTES:
                return StealthAddressPayment(address, amount)
            else:
                raise Exception("error: bad address {}".format(address))


@exception_printer
def sendtoaddress(spv, address, amount, memo=''):
    transaction_builder = spv.new_transaction_builder(memo=memo)
    transaction_builder.process_change(PubKeyChange)
    transaction_builder.process(get_output_producer(spv, address, spv.coin.parse_money(amount)))
    tx = transaction_builder.finish(shuffle_inputs=True, shuffle_outputs=True)

    if not tx.verify_scripts():
        raise Exception("internal error building transaction")

    spv.broadcast_transaction(tx)

    return {
        'tx': bytes_to_hexstring(tx.serialize(), reverse=False),
        'hash': bytes_to_hexstring(tx.hash()),
    }


@exception_printer
def sendspendtoaddress(spv, spend_hash, address, amount, memo=''):
    spend_hash = hexstring_to_bytes(spend_hash)
    transaction_builder = spv.new_transaction_builder(memo=memo)
    transaction_builder.include_spend(spend_hash)
    transaction_builder.process_change(PubKeyChange)
    transaction_builder.process(get_output_producer(spv, address, spv.coin.parse_money(amount)))
    tx = transaction_builder.finish(shuffle_inputs=True, shuffle_outputs=True)

    if not tx.verify_scripts():
        raise Exception("internal error building transaction")

    spv.broadcast_transaction(tx)

    return {
        'tx': bytes_to_hexstring(tx.serialize(), reverse=False),
        'hash': bytes_to_hexstring(tx.hash()),
    }


@exception_printer
def getbalance(spv):
    return dict((k, spv.coin.format_money(v)) for k, v in spv.wallet.balance.items())


@exception_printer
def getnewaddress(spv, label='', compressed=True):
    if str(compressed).lower() in ('1', 'true'):
        compressed = True
    else:
        compressed = False

    logger.debug("begin to create private key, compressed:{}".format(compressed))
    pk = PrivateKey.create_new()
    logger.debug(pk)
    spv.wallet.add('private_key', pk, {'label': label})
    return pk.get_public_key(compressed).as_address(spv.coin)


@exception_printer
def getnewstealthaddress(spv, label=''):
    pk = PrivateKey.create_new()
    spv.wallet.add('private_key', pk, {'label': label, 'stealth_payments': True})
    return base58_check(spv.coin,
                        pk.get_public_key(True).pubkey,
                        version_bytes=spv.coin.STEALTH_ADDRESS_VERSION_BYTES,
                        suffix_bytes=spv.coin.STEALTH_ADDRESS_SUFFIX_BYTES)


@exception_printer
def getnewpubkey(spv, label='', compressed=True):
    if str(compressed).lower() in ('1', 'true'):
        compressed = True
    else:
        compressed = False

    pk = PrivateKey.create_new()
    spv.wallet.add('private_key', pk, {'label': label})
    return pk.get_public_key(compressed).as_hex()


@exception_printer
def listspends(spv, include_spent=True):
    result = {
        'spendable': [],
        'not_spendable': [],
    }

    if str(include_spent).lower() in ('1', 'true'):
        include_spent = True
        result['spent'] = []
    else:
        include_spent = False

    def f(spend):
        r = {
            'id': bytes_to_hexstring(spend.hash()),
            'class': spend.__class__.__name__,
            'amount': spv.coin.format_money(spend.amount),
            'confirmations': spend.get_confirmations(spv),
        }

        if hasattr(spend, 'prevout'):
            r['prevout'] = {
                'txid': bytes_to_hexstring(spend.prevout.tx_hash),
                'n': spend.prevout.n
            }

        if hasattr(spend, 'address'):
            r['address'] = spend.address

        return r

    for spend in spv.wallet.spends.values():
        is_spent = spend['spend'].is_spent(spv)
        if not include_spent and is_spent:
            continue

        if is_spent:
            result['spent'].append(f(spend['spend']))
        elif spend['spend'].is_spendable(spv):
            result['spendable'].append(f(spend['spend']))
        else:
            # str(spend['spend']) + ', confirmations={}'.format(spend['spend'].get_confirmations(spv)))
            result['not_spendable'].append(f(spend['spend']))

    # logger.info('Spendable:\n' + str(result['spendable']) +
    #             '\nNot Spendable ({} confirmations required):\n'.format(spv.coin.TRANSACTION_CONFIRMATION_DEPTH) +
    #             str(result['not_spendable']))
    return result


@exception_printer
def dumppubkey(spv, address):
    '''PubKeyPaymentMonitor has to be included for this to work'''
    metadata = spv.wallet.get_temp('address', address)
    if metadata is None:
        return 'error: unknown address'

    return metadata['public_key'].as_hex()


@exception_printer
def dumpprivkey(spv, address_or_pubkey):
    '''PubKeyPaymentMonitor has to be included for this to work'''
    metadata = spv.wallet.get_temp('address', address_or_pubkey)
    if metadata is not None:
        public_key = metadata['public_key']
    else:
        public_key = PublicKey.from_hex(address_or_pubkey)

    metadata = spv.wallet.get_temp('public_key', public_key)
    if metadata is None:
        return 'error: unknown key'
    return metadata['private_key'].as_wif(spv.coin, public_key.is_compressed())


@exception_printer
def genmultisig(spv, nreq, mtotal, *pubkeys):
    '''Generate a new multisignature address and redemption script
    that requires `nreq' signatures to spend and provides a possible `mtotal'.
    If public keys are provided on the command line,
    those are used instead of generating new ones.'''

    nreq = int(nreq)
    mtotal = int(mtotal)
    pubkeys = list(pubkeys)
    assert 0 <= nreq <= mtotal
    assert len(pubkeys) <= mtotal

    # Create new keys if necessary
    while len(pubkeys) < mtotal:
        pk = PrivateKey.create_new()
        spv.wallet.add('private_key', pk, {'label': ''})
        pubkeys.append(pk.get_public_key(compressed=True).as_hex())

    pubkeys = [PublicKey.from_hex(pubkey) for pubkey in pubkeys]
    pubkeys.sort()

    # build the M-of-N multisig redemption script and add it to the wallet
    # (the p2sh monitor will notice that we added a redemption script to the
    # wallet and start watching for transactions to it

    script = Script()
    script.push_int(nreq)

    for pubkey in pubkeys:
        script.push_bytes(pubkey.pubkey)

    script.push_int(len(pubkeys))
    script.push_op(OP_CHECKMULTISIG)

    redemption_script = script.program
    address = base58_check(spv.coin, spv.coin.hash160(redemption_script),
                           version_bytes=spv.coin.P2SH_ADDRESS_VERSION_BYTES)

    try:
        spv.wallet.add('redemption_script', redemption_script, {})
    except DuplicateWalletItem:
        # No worries, we already have this redemption script
        if spv.logging_level <= horncore.INFO:
            print('[simple-wallet] Duplicate redemption script??')
        pass

    return {
        'address': address,
        'redemption_script': bytes_to_hexstring(redemption_script, reverse=False),
        'pubkeys': [pubkey.as_hex() for pubkey in pubkeys],
        'nreq': nreq,
    }


@exception_printer
def sendrawtransaction(spv, tx_bytes):
    tx_bytes = hexstring_to_bytes(tx_bytes, reverse=False)
    tx, _ = Transaction.unserialize(tx_bytes, spv.coin)
    spv.broadcast_transaction(tx)
    return bytes_to_hexstring(tx.hash())

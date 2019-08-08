# -*- coding: utf-8 -*-

""" base58 encoding / decoding functions """
import unittest

alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
balphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
base_count = len(alphabet)


def encode(num):
    """ Returns num in a base58-encoded string """
    encode = ''

    if (num < 0):
        return ''

    while (num >= base_count):
        mod = num % base_count
        encode = alphabet[mod] + encode
        num = num // base_count

    if (num):
        encode = alphabet[num] + encode

    return encode


def decode(s):
    """ Decodes the base58-encoded string s into an integer """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * alphabet.index(char)
        multi = multi * base_count

    return decoded


if bytes == str:  # python2
    iseq, bseq, buffer = (
        lambda s: map(ord, s),
        lambda s: ''.join(map(chr, s)),
        lambda s: s,
    )
else:  # python3
    iseq, bseq, buffer = (
        lambda s: s,
        bytes,
        lambda s: s.buffer,
    )


def scrub_input(v):
    if isinstance(v, str) and not isinstance(v, bytes):
        v = v.encode('ascii')

    if not isinstance(v, bytes):
        raise TypeError(
            "a bytes-like object is required (also str), not '%s'" %
            type(v).__name__)

    return v


def b58encode_int(i, default_one=True):
    '''Encode an integer using Base58'''
    if not i and default_one:
        return balphabet[0:1]
    string = b""
    while i:
        i, idx = divmod(i, 58)
        string = balphabet[idx:idx + 1] + string
    return string


def b58encode(v):
    '''Encode a string using Base58'''
    v = scrub_input(v)

    nPad = len(v)
    v = v.lstrip(b'\0')
    nPad -= len(v)

    p, acc = 1, 0
    for c in iseq(reversed(v)):
        acc += p * c
        p = p << 8

    result = b58encode_int(acc, default_one=False)

    return (balphabet[0:1] * nPad + result)


def b58decode_int(v):
    '''Decode a Base58 encoded string as an integer'''
    v = v.rstrip()
    v = scrub_input(v)

    decimal = 0
    for char in v:
        decimal = decimal * 58 + balphabet.index(char)
    return decimal


def b58decode(v):
    '''Decode a Base58 encoded string'''
    v = v.rstrip()
    v = scrub_input(v)

    origlen = len(v)
    v = v.lstrip(balphabet[0:1])
    newlen = len(v)

    acc = b58decode_int(v)

    result = []
    while acc > 0:
        acc, mod = divmod(acc, 256)
        result.append(mod)

    return (b'\0' * (origlen - newlen) + bseq(reversed(result)))


class Base58Tests(unittest.TestCase):
    def test_alphabet_length(self):
        self.assertEqual(58, len(alphabet))

    def test_encode_10002343_returns_Tgmc(self):
        result = encode(10002343)
        self.assertEqual('Tgmc', result)

    def test_decode_Tgmc_returns_10002343(self):
        decoded = decode('Tgmc')
        self.assertEqual(10002343, decoded)

    def test_encode_1000_returns_if(self):
        result = encode(1000)
        self.assertEqual('if', result)

    def test_decode_if_returns_1000(self):
        decoded = decode('if')
        self.assertEqual(1000, decoded)

    def test_encode_zero_returns_empty_string(self):
        self.assertEqual('', encode(0))

    def test_encode_negative_number_returns_empty_string(self):
        self.assertEqual('', encode(-100))


if __name__ == '__main__':
    unittest.main()

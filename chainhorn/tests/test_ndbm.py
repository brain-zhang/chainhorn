# -*- coding: utf-8 -*-

import _dbm
from .models import TestCase


class NDBMTestCase(TestCase):

    def setUp(self):
        # loading fixtures spv fake node data
        super(NDBMTestCase, self).setUp()

    def test_load_db(self):
        print(_dbm.__file__)

    def tearDown(self):
        super(NDBMTestCase, self).tearDown()

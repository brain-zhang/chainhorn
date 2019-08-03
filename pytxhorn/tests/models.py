# -*- coding: utf-8 -*-

import logging
import os
import unittest

from . import include
import settings


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('default')
        self.fixture_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))
        super(TestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.logger.info('hello, pytxhorn')
        super(TestCase, self).setUp()

    def tearDown(self):
        super(TestCase, self).tearDown()

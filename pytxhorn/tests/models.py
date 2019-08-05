# -*- coding: utf-8 -*-

import logging
import os
import shutil
import tempfile
import unittest

from . import include
import settings


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('default')
        self.fixture_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))
        self.temp_fixture_path = tempfile.mkdtemp(suffix='pytxhorn')
        shutil.copytree(os.path.join(self.fixture_path, 'bitcoin'), os.path.join(self.temp_fixture_path, 'bitcoin'))
        super(TestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.logger.info('hello, pytxhorn')
        super(TestCase, self).setUp()

    def tearDown(self):
        shutil.rmtree(self.temp_fixture_path)
        super(TestCase, self).tearDown()

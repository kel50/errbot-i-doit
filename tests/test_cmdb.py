#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging
from cmdb import *

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Search(unittest.TestCase):
    def test_searchresult(self):
        self.result = search('mylittleserver')
        self.assertIsInstance(searchformatter(self.result), list)
        print(self.result)

    def test_searchnet(self):
        self.result = search('testnet', 'Net')
        print(self.result)

    def test_emptysearch(self):
        self.result = search('')
        print(self.result)


if __name__ == '__main__':
    unittest.main()

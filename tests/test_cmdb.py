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
        self.result = search('hrlxreportsp01')
        print(self.result)

    @unittest.skip('test')
    def test_searchnet(self):
        self.result = search('client', 'Net')
        print(self.result)

if __name__ == '__main__':
    unittest.main()

# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module is the test class to test spiderengine
author zhangxuebin(z.capping@gmail.com)
"""
import log
import logging
import unittest

from app import spider_engine

class UrlParseTest(unittest.TestCase):
    """
    Test UrlPars
    """
    def setUp(self):
        self.url = "http://www.baidu.com"

    def test_engine(self):
        """
        test engine works well
        :return: nothing
        """
        a = spider_engine.SpiderEngine()
        a.set_config_by_file("../spider.conf")
        a.start_work()

    def test_set_config(self):
        """
        test the engine's setting config
        :return: nothing
        """
        a = spider_engine.SpiderEngine()
        a.set_config("urls", "output", 1, 1, 1, "*\.(html|png|jpg|bmp)$", 1)

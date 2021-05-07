# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This the url table of mini spider
author zhangxuebin(z.capping@gmail.com)
"""

import threading

class UrlTable(object):
    """
    the url table of spider.
    """

    def __init__(self):
        self.lock = threading.Lock()
        self.table = {}

    def add(self, url):
        """
        add url to table
        """
        self.lock.acquire()
        if url not in self.table:
            self.table[url] = True
        else:
            return False
        self.lock.release()
        return True

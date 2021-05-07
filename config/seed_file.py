# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This the seed file load of mini spider
author zhangxuebin(z.capping@gmail.com)
"""

import logging
import configparser
import queue

class SeedFile(object):
    """
    the seed file load of spider.
    load to load seed file from file path.
    """
    def __init__(self):
        self.queue = queue.Queue()

    def load(self, file_path):
        """
        get the urls from file
        :return: urls(tunple(url, level)). Error return False
        """
        try:
            with open(file_path) as urls:
                for url in urls:
                    if len(url.strip(' ')) < 1:
                        continue
                    self.queue.put((url, 0))
        except Exception as err:
            logging.error("get url from file error: %s ." % err)
            return False
        if self.queue.empty():
            return False
        return self.queue

# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This the engine of mini spider
author zhangxuebin(z.capping@gmail.com)
"""
import logging
import os
import queue
import configparser

from app import crawler
from app import url_table

class SpiderEngine(object):
    """
    the engine of spider.
    set_config to setup spider.
    start_work to power on
    """

    def __init__(self, config, input_queue):
        self.config = config
        self.input_queue = input_queue
        self.url_table = url_table.UrlTable()

    def start(self):
        """
        start to work
        :return: nothing
        """
        crawlers = []
        for thread_id in range(0, self.config.thread_count):
            thread = crawler.Crawler(self.input_queue, self.url_table, self.config)
            crawlers.append(thread)
            thread.start()
        for thread in crawlers:
            thread.join()
            logging.info("a thread done")
        self.input_queue.join()
        logging.info("queue is all done")

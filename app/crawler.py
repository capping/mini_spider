# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module is the mutil thread class for mini_spider
author zhangxuebin(z.capping@gmail.com)
"""


import logging
import re
import time
import threading

from app import UrlParse
from app import spider_engine

class Crawler(threading.Thread):
    """
    the module provider multi thread for mini spider
    """

    def __init__(self, queue, url_table, config):
        threading.Thread.__init__(self)
        self.queue = queue
        self.url_table = url_table
        self.timeout = config.crawl_timeout
        self.interval = config.crawl_interval
        self.output_directory = config.output_directory
        self.max_depth = config.max_depth
        self.target_url = config.target_url
        
    def need_download(self, url):
        """
        judge whether the url needs download.
        downloaded, no
        not match the rules, no
        :param url: the url
        :return: True, False
        """
        if not UrlParse.UrlParse.is_url(url):
            return False
        try:
            pattern = re.compile(self.target_url)
        except Exception as err:
            logging.error("the target url is not re..compile fail: %s" % self.target_url)
            return False
        if len(url.strip(' ')) < 1 or not pattern.match(url.strip(' ')):
            return False
        return True

    def run(self):
        """
        run the thread.
        get task from queue. And add the sub url into queue. BFS.
        :return: no return
        """
        while True:
            try:
                url, level = self.queue.get(block=True, timeout=self.timeout)
                logging.info("queue get %s, %s" % (url, str(level)))
            except Exception as err:
                logging.info("this thread can not get a task. job done.")
                break
            self.queue.task_done()
            logging.info("queue task_done, queue size: %s" % self.queue.qsize())
            #sleep interval
            time.sleep(self.interval)

            #download the url
            if self.need_download(url):
                UrlParse.UrlParse.download(self.output_directory, url)
            if self.url_table.add(url):
                #get the sub urls from url
                sub_urls = UrlParse.UrlParse.get_urls(url)
                new_level = level + 1
                if new_level > self.max_depth:
                    continue
                for url in sub_urls:
                    self.queue.put((url, new_level))
                    logging.info("queue put %s, %s" % (url, str(new_level)))

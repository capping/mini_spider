# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This the config load of mini spider
author zhangxuebin(z.capping@gmail.com)
"""

import os
import logging
import configparser

class ConfigLoad(object):
    """
    the config load of spider.
    load to load config from file path.
    """
    def __init__(self):
        self.output_directory = "output"
        self.url_list_file = "urls"
        self.max_depth = 1
        self.crawl_interval = 1
        self.crawl_timeout = 10
        self.target_url = ".*\.(gif|png|jpg|bmp)$"
        self.thread_count = 1
    
    def set_config(self, url_list_file, output_directory, max_depth, crawl_interval,
                   crawl_timeout, target_url, thread_count):
        """
        set the conf of spider
        :param url_list_file:
        :param output_directory:
        :param max_depth:
        :param crawl_interval:
        :param crawl_timeout:
        :param target_url:
        :param thread_count:
        :return: Error return False
        """
        self.url_list_file = url_list_file
        self.output_directory = output_directory
        self.max_depth = max_depth
        self.crawl_interval = crawl_interval
        self.crawl_timeout = crawl_timeout
        self.target_url = target_url
        self.thread_count = thread_count

        #complete the output path
        self.set_full_dir(self.output_directory)

    def load(self, cfg_path):
        """
        the load method to load config from file path
        """
        if len(cfg_path) < 1:
            logging.error("the path of file error.file: %s." % cfg_path)
            return False
        cf = configparser.ConfigParser(inline_comment_prefixes=(";",))
        try:
            cf.read(cfg_path)
        except Exception as err:
            logging.error("get conf file error: %s" % err)
            return False
        self.set_config(cf.get("spider", "url_list_file"), cf.get("spider", "output_directory"), 
            cf.getint("spider", "max_depth"), cf.getint("spider", "crawl_interval"), 
            cf.getint("spider", "crawl_timeout"), cf.get("spider", "target_url"), 
            cf.getint("spider", "thread_count"))
        
        return self
    
    def set_full_dir(self, path):
        """
        complete the path ,and mkdir if it not exits
        :param path: the path
        :return: the output path
        """
        output_dir = os.path.join(os.getcwd(), path)
        if not os.path.exists(output_dir):
            try:
                os.mkdir(output_dir)
            except os.error as err:
                logging.error("mkdir output dir error: %s. " % err)
        return str(output_dir)

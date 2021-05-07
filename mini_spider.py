# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This main module
"""
import getopt
import log
import logging
import sys

from app import spider_engine
from config import config_load
from config import seed_file

def version():
    """
    print the version
    """
    print("version 1.0.0")

def main():
    """
    the main method to run mini spider
    """
    # 日志保存到./log/spider.log和./log/spider.log.wf，按天切割，保留7天
    log.init_log("./log/spider")
    cfg_path = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhc:")
    except getopt.GetoptError as err:
        logging.error("get option error : %s." % err)
        return
    for o, a in opts:
        if o == "-v":
            version()
            return
        elif o == "-h":
            print("帮助信息：没有帮助^_^")
            return
        elif o == "-c":
            cfg_path = a
        else:
            logging.error("unhandled option")
            print("unhandled option")
            return

    config = config_load.ConfigLoad().load(cfg_path)
    if config is False:
        logging.error("load config file fail!")
        return

    queue = seed_file.SeedFile().load(config.url_list_file)
    if queue is False:
        logging.error("load seed file fail!")
        return

    spider = spider_engine.SpiderEngine(config, queue).start()

if __name__ == "__main__":
    main()

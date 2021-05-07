# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module is some static method for parse url, html
author zhangxuebin(z.capping@gmail.com)
"""
import os
import urllib
import urllib.request
from urllib import parse as urlparse
import requests
import logging
import string
import random

import chardet
from bs4 import BeautifulSoup


class UrlParse(object):
    """
    the public url tools to deal with url
    """
    @staticmethod
    def is_url(url):
        """
        if the url is start with javascript ignore it
        :param url:
        :return:True False
        """
        if url.startswith("javascript"):
            return False
        return True

    @staticmethod
    def get_urls(url):
        """
        get the urls under this url
        :param url: origin url
        :return:the set of sub_urls
        """
        url_set = set()
        if not UrlParse.is_url(url):
            return url_set

        content = UrlParse.get_html_content(url)
        if content is None:
            return url_set
        tag_list = ['img', 'a', 'script', 'style']
        link_list = []

        for tag in tag_list:
            link_list.extend(BeautifulSoup(content, 'html.parser').findAll(tag))

        for link in link_list:
            if link.has_attr('src'):
                url_set.add(UrlParse.deal_with_url(link['src'], url))
            if link.has_attr('href'):
                url_set.add(UrlParse.deal_with_url(link['href'], url))

        return url_set

    @staticmethod
    def deal_with_url(url, base_url):
        """
        deal with url to make it complete and standard
        :param url: the url href
        :param base_url: the base url where the orginal url is
        :return:completed url
        """
        if url.startswith('http') or url.startswith('//'):
            url = urlparse.urlparse(url, scheme='http').geturl()
        else:
            url = urlparse.urljoin(base_url, url)
        return url

    @staticmethod
    def get_html_content(url, timeout=10):
        """
        Get html contents
        :param url: the target url
        :param timeout: urlopen timeout, default 10
        :return: the content of html page, return None when error happens
        """
        user_agents = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        try:
            random_agent = user_agents[random.randint(0, len(user_agents)-1)]
            headers={
                'User-Agent': random_agent,
                'Connection': 'close'
            }
            s = requests.session()
            s.keep_alive = False
            s.headers = headers
            response = s.get(url, timeout=timeout)
        except urllib.request.URLError as err:
            logging.error("url open error, url: %s, Reason: %s" % (url, err.reason))
            return None
        try:
            content = response.content
        except Exception as err:
            logging.error("read response error")
            return None

        return UrlParse.decode_html(content)

    @staticmethod
    def decode_html(content):
        """
        decode content
        :param content: the origin content
        :return: returen decoded content. Error return None
        """
        encoding = chardet.detect(content)['encoding']
        if encoding == 'GB2312':
            encoding = 'GBK'
        else:
            encoding = 'utf-8'
        try:
            content = content.decode(encoding, 'ignore')
        except Exception as err:
            logging.error("Decode error: %s.", err)
            return None
        return content

    @staticmethod
    def download(local_path, url):
        """
        download html, file to local file
        :param local_path: base_path
        :param url: download url
        :return: succeed True, fail False
        """

        if not os.path.exists(local_path):
            try:
                os.mkdir(local_path)
            except os.error as err:
                logging.error("download to path, mkdir errror: %s" % err)

        try:
            path = os.path.join(local_path, url.replace('/', '_').replace(':', '_')
                                .replace('?', '_').replace('\\', '_'))
            logging.info("download url..: %s" % url)
            urllib.request.urlretrieve(url, path, None)
        except Exception as err:
            logging.error("download url fail. url: %s" % url)
            return False
        return True
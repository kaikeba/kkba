import base64
import logging

import requests
from requests.auth import HTTPBasicAuth
from w3lib.http import basic_auth_header


class Proxy(object):
    def __init__(
            self,
            crawlerType='requests',
            proxyType=None,
            username=None,
            password=None,
            proxy_url=None,
            **kwargs
    ):
        """
        :param crawlerType: crawler type, value is requests or scrapy
        :type crawlerType:
        :param proxyType: proxy type,  value is abuyun、kuaidaili、qingting
        :type proxyType:
        :param username:
        :type username:
        :param password:
        :type password:
        :param proxy_url:
        :type proxy_url:
        :param kwargs:
        :type kwargs:
        """
        self.crawlerType = crawlerType
        self.proxyType = proxyType
        self.username = username
        self.password = password
        self.proxy_url = proxy_url

    def get_proxy(self, request=None):
        if self.proxyType and self.username and self.password:
            proxyType = self.proxyType
        else:
            logging.error('Please input proxy type, proxy username and password, proxy server api')
            return
        if self.crawlerType == 'requests':
            if proxyType == 'qingting':
                return self.__qingting_requests()
            if proxyType == 'kuaidaili':
                return self.__kuaidaili_requests()
            elif proxyType == 'abuyun':
                return self.__abuyun_request()
            else:
                logging.error('No proxy type of {}'.format(proxyType))
        if self.crawlerType == 'scrapy':
            if not request:
                logging.error('Scrapy must params request object')
                return
            if proxyType == 'qingting':
                return self.__qingting_scrapy(request)
            elif proxyType == 'kuaidaili':
                return self.__kuaidaili_scrapy(request)
            elif proxyType == 'abuyun':
                return self.__abuyun_scrapy(request)
            else:
                logging.error('No proxy type of {}'.format(proxyType))
        else:
            logging.error('No support this proxy type')

    def __qingting_requests(self):
        """
        qingting proxy requests
        :return:
        :rtype:
        """
        if not self.proxy_url:
            logging.error('qingting proxy need input proxy api')
            return
        proxy_text = requests.get(self.proxy_url, auth=HTTPBasicAuth(self.username, self.password)).text.strip()
        proxies = {
            'http': proxy_text,
            'https': proxy_text
        }
        return proxies

    def __qingting_scrapy(self, request):
        """
        qingting proxy scrapy
        :param request:
        :type request:
        :return:
        :rtype:
        """
        if not self.proxy_url:
            logging.error('qingting proxy need input proxy api')
            return
        proxy_text = requests.get(self.proxy_url, auth=HTTPBasicAuth(self.username, self.password)).text.strip()
        request.meta['proxy'] = "http://" + proxy_text
        return request

    def __kuaidaili_requests(self):
        """
        kuai proxy requests
        :return:
        :rtype:
        """
        if not self.proxy_url:
            self.proxy_url = "tps163.kdlapi.com:15818"
        tunnel = self.proxy_url

        # username and password authration
        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": self.username, "pwd": self.password,
                                                            "proxy": tunnel},
            "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": self.username, "pwd": self.password,
                                                             "proxy": tunnel}
        }
        return proxies

    def __kuaidaili_scrapy(self, request):
        """
        kuai proxy scrapy
        :param request:
        :type request:
        :return:
        :rtype:
        """
        if not self.proxy_url:
            self.proxy_url = "tps163.kdlapi.com:15818"
        proxy = self.proxy_url
        request.meta['proxy'] = "http://%(proxy)s" % {'proxy': proxy}
        # username and password authration
        # Whitelist authentication can comment this line
        request.headers['Proxy-Authorization'] = basic_auth_header(self.username, self.password)
        request.headers["Connection"] = "close"
        return request

    def __abuyun_request(self):
        """
        abuhun request
        :return:
        :rtype:
        """
        if not self.proxy_url:
            self.proxy_url = "http-dyn.abuyun.com"
        proxyHost = self.proxy_url
        proxyPort = "9020"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": self.username,
            "pass": self.password,
        }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies

    def __abuyun_scrapy(self, request):
        """
        abuyun scrapy
        :param request:
        :type request:
        :return:
        :rtype:
        """
        if not self.proxy_url:
            self.proxy_url = "http://http-dyn.abuyun.com:9020"
        proxyServer = self.proxy_url
        # for Python2
        proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((self.username + ":" + self.password), "ascii")).decode(
            "utf8")
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth
        return request


if __name__ == '__main__':
    p = Proxy(crawlerType='requests', proxyType='xxx', username='xxx', password='xxx')
    proxy = p.get_proxy()
    url = 'http://httpbin.org/get'
    res = requests.get(url, proxies=proxy)
    print(res.text)

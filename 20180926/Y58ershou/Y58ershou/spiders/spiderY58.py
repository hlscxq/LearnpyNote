# -*- coding: utf-8 -*-
import scrapy
import re
import random
from Y58ershou.items import Y58ErshouItem

class Spidery58Spider(scrapy.Spider):
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    name = 'spiderY58'
    allowed_domains = ['sy.58.com']
    start_urls = ['https://sy.58.com/ershoufang']
    dept = 5

    def parse(self, response):
        for depthi in range(self.dept):
            try:
                ua = random.choice(self.user_agent_list)  # 随机抽取User-Agent
                headers = {
                    'Accept-Encoding': 'gzip, deflate, sdch, br',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Connection': 'keep-alive',
                    'Referer': 'https://sy.58.com/ershoufang/',
                    'User-Agent': ua
                }

                url = 'https://sy.58.com/ershoufang/pn'+str(depthi+1)+'/'
                yield scrapy.Request(url, callback=self.parse_houses, headers=headers,dont_filter=True)
            except:
                continue
    def parse_houses(self, response):
        i=0
        for sel in response.xpath('//ul[contains(@class, "house-list-wrap")]/li'):
            try:
                item = Y58ErshouItem()
                item['title'] = self.FormatRItem(sel.xpath('normalize-space(./div[contains(@class, "list-info"'
                                                            ')]/h2)').extract())

                item['baseInfo'] = self.FormatRItem(sel.xpath('./div[contains(@class, "list-info")]'
                                                              '/p//text()').extract())
                #item['loc'] = sel.xpath('text()').extract()
                item['ageInfo']=self.FormatRItem(sel.xpath('normalize-space(./div/div[contains'
                                                           '(@class, "jjrinfo")])').extract())
                item['price']=self.FormatRItem(sel.xpath('normalize-space(./div[contains(@class,'
                                                         ' "price")])').extract())
                item['time']=self.FormatRItem(sel.xpath('normalize-space(./div[contains(@class, '
                                                        '"time")])').extract())
                print ("item crwal t %s"%(i))
                # print (item)
                i += 1
            except Exception as e:
                print(e)
                continue
            yield item

    def FormatRItem(self,Trs):
        BInfo = ''
        for B in Trs:
            A = B.strip().replace('//n', '')
            if A:
                BInfo = BInfo + A + ';;'
        return BInfo
# -*- coding: utf-8 -*-
import scrapy
#import requests
import re
import time

from lxml import etree

from lianjia.items import LianjiaItem
from lianjia.Download import down
#from bs4 import BeautifulSoup


class LjspiderSpider(scrapy.Spider):
    name = "ljspider"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = []
    base_url = 'https://bj.lianjia.com/ershoufang/shunyi/pg'
    for i in range(1, 28):
        url = base_url + str(i) + '/'
        start_urls.append(url)

    def parse(self, response):
        contents = etree.HTML(response.body.decode('utf-8'))
        houselist = contents.xpath('/html/body/div[4]/div[1]/ul/li')
        time.sleep(2)
        for house in houselist:
            try:
                item = LianjiaItem()
                item['title'] = house.xpath('div[1]/div[1]/a/text()').pop()
                item['community'] = house.xpath('div[1]/div[2]/div/a/text()').pop()
                item['model'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[1]
                item['area'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[2]
                item['focus_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[0]
                item['watch_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[1]
                item['time'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[2]
                item['price'] = house.xpath('div[1]/div[6]/div[1]/span/text()').pop()
                item['average_price'] = house.xpath('div[1]/div[6]/div[2]/span/text()').pop()
                item['link'] = house.xpath('div[1]/div[1]/a/@href').pop()
                # item['city'] = response.meta["id1"]
                self.url_detail = house.xpath('div[1]/div[1]/a/@href').pop()
                item['Latitude'] = self.get_latitude(self.url_detail)
            except Exception:
                pass
            yield item

    def get_latitude(self, url):  # 进入每个房源链接抓经纬度
        p = down.get(url, 2)
        #time.sleep(1)
        longitude_latitude = re.findall(r"resblockPosition:'(.*?)'.*?cityId", p.text, re.S)# 经纬度
        return longitude_latitude[0][0:-1]

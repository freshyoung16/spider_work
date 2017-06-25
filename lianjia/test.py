import requests
from bs4 import BeautifulSoup
import os
import re
import time
from lxml import etree

headers = {'User-Agent': "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"}
all_url = 'https://bj.lianjia.com/ershoufang/101101553713.html'
html = requests.get("http://www.xicidaili.com/nn", headers=headers)  ##不解释咯
#start_html = requests.get(all_url, headers=headers)
iplistn = re.findall(r'<td>(\d*\.\d*\.\d*\.\d*)</td>.*?<td>(\d*)</td>.*?<td>(\w*)</t', html.text, re.S)
#start_html.encoding = 'gbk'
#Soup = BeautifulSoup(start_html.text, 'html5lib')
#all_num = Soup.find('div', attrs={"comp-module": "page"})
#contents = etree.HTML(start_html.content.decode('utf-8'))
#latitude = contents.xpath('/ html / body / script[20]/text()').pop()
#latitude = re.findall(r"resblockPosition:'(.*?)'.*?cityId", start_html.text, re.S)
time.sleep(1)
for ip in iplistn:
    if ip[2] == 'HTTPS':
        i = ip[0] + ':' + ip[1]
        print(i)
#print(latitude)
#img_url = Soup.find_all('input', type='image')
#print(longitude_latitude[1:-1])
#for i in all_num:
#	print(i)
'''all_font = Soup.find_all(color="green")
for i in all_font:
    print(i.parent['href']) 标签选取测试
'''
#for i in all_font.length:
#    print(all_font[i])
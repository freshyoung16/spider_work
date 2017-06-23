import requests
from lxml import etree

url = 'http://www.chemistwarehouse.com.au/buy/64313/Goat-Body-Wash-Original-500ml'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
html = requests.get(url, headers=headers)
contents = etree.HTML(html.content.decode('utf-8'))
#picurl = contents.xpath('//*[@id="lightbox"]/div[1]/div/img/@src').pop()
print(html.text)

import requests
from requests.exceptions import RequestException
from lxml import etree
from pymongo import MongoClient

def get_one_page(url):
    try:
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        return None
    except RequestException:
        return None

def parse_one_page(html):
    contents = etree.HTML(html.content.decode('utf-8'))
    productlist = contents.xpath('//*[@id="p_lt_ctl06_pageplaceholder_p_lt_ctl00_wD_H_Top_lstElem"]/tr')
    for product in productlist:
        for i in range(1, 4):
            td = 'td[' + str(i) + ']'
            if product.xpath(td + '/a/@title'):
                yield {
                    'name': product.xpath(td + '/a/@title').pop().strip(),
                    'price': product.xpath(td + '/a/div/div[2]/span[1]/text()').pop().strip(),
                    'save': product.xpath(td + '/a/div/div[2]/span[2]/text()').pop().strip()[6:] if product.xpath(td + '/a/div/div[2]/span[2]/text()') else None,
                    'detailurl': 'http://www.chemistwarehouse.com.au' + product.xpath(td + '/a/@href').pop(),
                    'picurl': product.xpath(td + '/a/div/div[1]/div[1]/img[1]/@src').pop()
                }
            else:
                pass

def SavePic(item):
    url = item['detailurl']
    filename = item['name'] + '.jpg'
    basepath = str('E:/Result/cwtop/')
    html = get_one_page(url)
    contents = etree.HTML(html.content.decode('utf-8'))
    picurl = contents.xpath('//*[@id="slider_pi_container"]/div[2]/div[1]/a/@href').pop()
    content = requests.get(picurl).content
    with open(basepath + filename, 'wb') as f:
        f.write(content)
    print('当前文件 {} 下载完毕'.format(basepath + filename))

def main(offset):
    client = MongoClient()
    db = client['aozhoudaigou']
    product_collection = db['cwhouse']
    url = 'http://www.chemistwarehouse.com.au/BestSellers?page=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        product_collection.save(item)
        #SavePic(item)
    print('page' + str(offset) + ' is done')

if __name__ == '__main__':
    for i in range(1, 4):
        main(i)

from bs4 import BeautifulSoup
import os
from Download import down
from multiprocessing.dummy import Pool as ThreadPool
import time
from pymongo import MongoClient
import datetime

client = MongoClient()
db = client['meinvxiezhenji']
dagaier_collection = db['dagaier']
class Item():
    '''
    模拟Scrapy
    创建一个类
    保存帖子名称和url地址
    '''
    title = ''
    title_url = ''
    pic_urls = []
    url = None
    name = None

def mkdir(path):
    '''
    防止目录存在
    '''
    path = path.strip()
    isExists = os.path.exists(os.path.join("E:/result/dagaier/", path))
    if not isExists:
        print(u'建了一个名字叫做', path, u'的文件夹！')
        os.makedirs(os.path.join("E:/result/dagaier/", path))
        os.chdir(os.path.join("E:/result/dagaier/", path))  # 切换到目录
        return True
    else:
        print(u'名字叫做', path, u'的文件夹已经存在了！')
        return False

def SavePic(item):
    '''
    通过中间件down
    将抓取到的图片保存到本地
    '''
    url = item.url
    filename = item.name
    basepath = str('E:/result/dagaier/')
    content = down.get(url, 3).content
    with open(basepath + filename, 'wb') as f:
        f.write(content)
    print('当前文件 {} 下载完毕'.format(basepath + filename))

def get_article(index_url):
    '''
    获取当前页每一个原创帖子的url连接
    并返回一个字典类型k：帖子名称 v：帖子url地址
    '''
    title_list = []
    path_list = []
    url_list = []


    html = down.get(index_url, 3)
    html.encoding = 'gbk'
    all_font = BeautifulSoup(html.text, 'lxml').find_all(color="green")
    for font in all_font:
        title = font.get_text()
        title_list.append(title)
        print(u'发现帖子：', title)  ##加点提示不然太枯燥了
        path = str(title).replace('？','')  ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
        path_list.append(path)
        mkdir(path)  ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
        href = font.parent['href']
        if dagaier_collection.find_one({'主题页面': href}):  ##判断这个主题是否已经在数据库中、不在就运行else下的内容，在则忽略。
            print(u'这个页面已经爬取过了')
        else:
            url_list.append('https://liuyouba.tk/' + href)

    Aticles = dict(title=title_list, name=path_list, urls=url_list)
    
    return Aticles

def get_pic(Aticles):
    '''
    打开每个帖子的url，
    找到图片的地址，
    保存在列表并返回
    '''
    # 用于保存item的列表
    aticles_urls = []

    # 从dict里分离漫画名和章节链接
    aticle_list = Aticles['urls']
    basedir = Aticles['name']
    mongo_title = Aticles['title']
    # print(len(basedir))
    # print(len(aticle_list))
    pathNum = 0
    for url in aticle_list:
        img_html = down.get(url, 3)
        img_urls = BeautifulSoup(img_html.text, 'lxml').find_all('input', type='image')
        post = {  ##这是构造一个字典，里面有啥都是中文，很好理解吧！
            '标题': mongo_title[pathNum],
            '主题页面': url,
            '图片地址': img_urls['src'],
            '获取时间': datetime.datetime.now()
        }
        dagaier_collection.save(post)  ##将post中的内容写入数据库。
        print(u'插入数据库成功')
        picNum = 1
        for img_url in img_urls:
            item = Item()
            item.url = img_url['src']
            item.name = str(basedir[pathNum]) + '/' + str(picNum) + '.jpg'
            aticles_urls.append(item)
            picNum = picNum + 1
        pathNum = pathNum + 1
        

    return aticles_urls

def main():
    start = time.clock()
    Aticles_index = get_article('https://liuyouba.tk/thread0806.php?fid=16&search=&page=2')
    Aticles_items = get_pic(Aticles_index)

    # 开启多线程 线程数10
    pool = ThreadPool(10)
    pool.map(SavePic, Aticles_items)
    pool.close()
    pool.join()
    end = time.clock()
    print(end - start)

if __name__ == '__main__':
    main()






# class caoliu():

#     def all_url(self, url):
#         html = down.get(url, 3)  # 调用request函数把套图地址传进去会返回给我们一个response
#         html.encoding = 'gbk'
#         all_font = BeautifulSoup(html.text, 'lxml').find_all(color="green")
#         for font in all_font:
#             title = font.get_text()
#             print(u'开始保存：', title)  ##加点提示不然太枯燥了
#             path = str(title)  ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
#             self.mkdir(path)  ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
#             href = font.parent['href']
#             self.img('https://liuyouba.tk/' + href)
#         ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！
#         '''
        

#     def html(self, href):   ##这个函数是处理套图地址获得图片的页面地址
#         html = self.request(href)
#         max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
#         for page in range(1, int(max_span) + 1):
#             page_url = href + '/' + str(page)
#             self.img(page_url) ##调用img函数
#         '''
#     def img(self, page_url):  # 这个函数处理图片页面地址获得图片的实际地址
#         img_html = request.get(page_url, 3)
#         img_html.encoding = 'gbk'
#         # img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='tpc_content do_not_catch').find('input')['src']
#         img_url = BeautifulSoup(img_html.text, 'lxml').find_all('input', type='image')
#         for i in img_url:
#             self.save(i['src'])

#     def save(self, img_url):  # 这个函数保存图片
#         name = img_url[-8:-4]
#         img = request.get(img_url, 3)
#         f = open(name + '.jpg', 'ab')
#         f.write(img.content)
#         f.close()

#     def mkdir(self, path):  # 这个函数创建文件夹
#         path = path.strip()
#         isExists = os.path.exists(os.path.join("E:\caoliu", path))
#         if not isExists:
#             print(u'建了一个名字叫做', path, u'的文件夹！')
#             os.makedirs(os.path.join("E:\caoliu", path))
#             os.chdir(os.path.join("E:\caoliu", path))  # 切换到目录
#             return True
#         else:
#             print(u'名字叫做', path, u'的文件夹已经存在了！')
#             return False

# Caoliu = caoliu()  # 实例化
# Caoliu.all_url('https://liuyouba.tk/thread0806.php?fid=16')  # 给函数all_url传入参数  你可以当作启动爬虫（就是入口）
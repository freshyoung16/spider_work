from lianjia.middlewares.proxy import proxies
import random

class RandomProxy(object):
    def process_request(self,request,spider):
        # 从文件中随机选择一个代理
        proxy = random.choice(proxies)

        request.meta['proxy'] = 'https://{}'.format(proxy)
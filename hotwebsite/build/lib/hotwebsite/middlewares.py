# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from random import choice
from scrapy.exceptions import NotConfigured
from queue import Queue
from threading import Thread
import schedule
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from .js.jsl import JSL
from .util.common import get_ua_headers




class HotwebsiteSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class HotwebsiteDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        # if request.headers.get('User-Agent') is None:
        #     header = get_ua_headers()
        #     request.headers.update(header)
   
          

        if not request.cookies:

            if request.headers.get('User-Agent') is None:

                if spider.name in ['zbytb',"zhaobiao"]:

                    request = self.get_request_from_cookie(request)
            
                else:
                    header = get_ua_headers()
                    request.headers.update(header)
   
        return None
       

    def process_response(self, request, response, spider):

        # Called with the response returned from the downloader. 
        # 如果状态码是521
        if response.status == 521:
            
            request = self.get_request_from_cookie(request)
 
            return request

        if response.status == 403:
            
            request = self.get_request_from_cookie(request)
 
            return request


     
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


    def get_request_from_cookie(self,request):

            header = get_ua_headers()
            request.headers.update(header)

            jsl = JSL(header,request.url)
            new_cookie = jsl.get_header_cookie()

            if new_cookie:
                request.cookies = new_cookie
            
            return request
            




# /proxy:
#   ip: http://58.213.106.158:8901/api/proxy/getProxy
#   token: 970e02783dd34fbfb7439d8a9a706ce4
#   max_retry: 1


# class ProxyMiddleware:
#     def __init__(self, proxies):
#         self.proxies = proxies

#     @classmethod
#     def from_crawler(cls, crawler):
#         if not crawler.settings.getbool('USE_PROXY'):
#             raise NotConfigured
#         return cls(proxy_pool.get_proxy())

#     def process_request(self, request, spider):
#         request.meta['proxy'] = self.proxies

#     def process_exception(self, request, exception, spider):
#         proxy_address = request.meta.get('proxy')
#         if proxy_address:
#             print("Removing failed proxy: " + proxy_address)
#             self.proxies.remove(proxy_address)

#         # Retry with a new proxy
#         retry_request = request.copy()
#         retry_request.meta['retry_times'] = retry_request.meta.get('retry_times', 0) + 1
#         return retry_request

#     def process_response(self, request, response, spider):
#         if response.status == 521:
#             proxy_address = request.meta.get('proxy')
#             if proxy_address:
#                 print("Removing failed proxy: " + proxy_address)
#                 self.proxies.remove(proxy_address)

#             # Retry with a new proxy
#             retry_request = request.copy()
#             retry_request.meta['retry_times'] = retry_request.meta.get('retry_times', 0) + 1
#             return retry_request
#         return response


# class ProxyPool:
#     def __init__(self, max_size=10):
#         self.proxy_queue = Queue(max_size)
#         self.check_thread = None

#     @classmethod
#     def __get_proxy(cls):
#         """从API获取单个代理"""
#         response = requests.post("http://58.213.106.158:8901/api/proxy/getProxy", headers={'token': "970e02783dd34fbfb7439d8a9a706ce4"})
#         if response.status_code == 200:
#             rt_json = response.json()
#             proxy = rt_json['data']
#             return proxy
#         else:
#             return None

#     def __is_proxy_valid(self, proxy):
#         """检查代理是否有效"""
#         try:
#             # 定义代理字典
#             proxies = {
#                 "http": f"http://{proxy}",
#                 "https": f"https://{proxy}",
#             }

#             # 发送请求，设置超时时间
#             response = requests.get('http://baidu.com', proxies=proxies, timeout=5)

#             # 检查状态码
#             if response.status_code == 200:
#                 return True
#         except requests.exceptions.RequestException:
#             # 如果发生任何请求相关的异常，都认为该代理无效
#             return False

#         # 如果请求成功但状态码不是200，则认为代理无效
#         return False

#     def add_proxy(self):
#         """向代理池添加代理"""
#         while self.proxy_queue.qsize() < self.proxy_queue.maxsize:
#             proxy = self.__get_proxy()
#             if proxy and self.__is_proxy_valid(proxy):
#                 self.proxy_queue.put(proxy)

#     def start_checking(self):
#         """启动线程定期检查代理的有效性"""
#         if self.check_thread is None:
#             self.check_thread = Thread(target=self.__check_proxies)
#             self.check_thread.start()

#     def __check_proxies(self):
#         """定期检查代理的有效性，并添加适当的延迟"""
#         while True:
#             try:
#                 proxy = self.proxy_queue.get(timeout=1)  # 获取代理，如果队列为空则等待1秒
#                 if not self.__is_proxy_valid(proxy):
#                     # 移除无效的代理
#                     self.proxy_queue.task_done()
#                 else:
#                     # 重新加入有效的代理
#                     self.proxy_queue.put(proxy)
#                     self.proxy_queue.task_done()
#                 time.sleep(1)  # 每检查完一个代理后等待1秒
#             except Exception as e:
#                 print(f"Error during proxy check: {e}")
#             finally:
#                 # 如果队列为空，则等待一段时间再重新尝试
#                 if self.proxy_queue.empty():
#                     time.sleep(60)  # 等待60秒

#     def get_proxy(self):
#         """从代理池中获取一个代理"""
#         return self.proxy_queue.get(block=True)



# # 定时任务，更新add_proxy()
# def job(proxy_pool):
#         proxy_pool.add_proxy()
#         print("Job done!")


# if __name__ == '__main__':
#     proxy_pool = ProxyPool(max_size=5)

#     # 启动检查线程
#     proxy_pool.start_checking()
#     # 添加代理
#     proxy_pool.add_proxy()

#     schedule.every(5).minute.do(job(proxy_pool))

#     while True:
#         schedule.run_pending()
#         time.sleep(1)
   



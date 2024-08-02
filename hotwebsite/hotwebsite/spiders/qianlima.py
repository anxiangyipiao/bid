import scrapy
from ..util.redis_manager import redis_manager_urls
from ..util.common import extract_longest_link, insert_url_item


class ExampleSpider(scrapy.Spider):
    name = "qianlima"
    start_urls = ["https://www.qianlima.com/zbgg/p{page}"]

    def __init__(self, name=None, **kwargs):
        self.url_list = []
        self.items = {}
        self.depth = 1
        self.has_next_page = True

    def start_requests(self):
            
            url = self.start_urls[0].format(page=self.depth)
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        
        for quote in response.xpath('//div[@class="list-single f-v-center"]'):
            
            title, url = extract_longest_link(quote)

           # 添加url到url_list,记录本次爬取的所有url，包括第一次出现的url，和最后一个重复的url
            self.url_list.append(url)

            # 添加到items
            self.items[url] = title


            # 如果URL已经被添加，则说明达到增量爬取位置，则停止爬取
            if redis_manager_urls.has_hash_seen(url):
                # 不再翻页
                self.has_next_page = False

                # 如果有多个url，则更新增量爬取位置,并添加数据到redis items
                # 如果只有一个url，则不更新增量爬取位置
                if len(self.url_list) > 1:
                    
                    # 更新
                    insert_url_item(self.url_list,self.items)

                # 打印日志
                self.logger.info("URL has been seen before, stopping.")

                break

         # 深度加1
        self.depth += 1
        # 判断是否达到深度，如果达到则停止爬取
        if self.depth_stop():
            return

        if self.has_next_page:

            yield response.follow(self.start_urls[0].format(page=self.depth), self.parse,dont_filter=True)
 
    def depth_stop(self):

        """深度停止爬取"""
        if self.depth > 90:
            
            self.has_next_page = False

            # 更新
            insert_url_item(self.url_list,self.items)

            return True
        
        return False
    



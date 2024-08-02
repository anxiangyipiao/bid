import scrapy
from ..util.redis_manager import redis_manager_urls
from ..util.common import extract_longest_link, insert_url_item


class ExampleSpider(scrapy.Spider):
    name = "zbytb"
    start_urls = ["https://www.zbytb.com/search/?kw=&okw=&catid=0&zizhi=&zdxm=&zdyear=&field=0&moduleid=25&areaids=&page={page}"]

    def __init__(self, name=None, **kwargs):
        self.url_list = []
        self.items = {}
        self.depth = 1
        self.has_next_page = True

    def start_requests(self):

            url = self.start_urls[0].format(page=self.depth)
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)   

    def parse(self, response):
        
        for quote in response.xpath('//div[@class="list-box  simple"]/ul/li'):
            

            title, url = extract_longest_link(quote)

            self.url_list.append(url)
            self.items[url] = title

            if redis_manager_urls.has_hash_seen(url):

                self.has_next_page = False
                if len(self.url_list) > 1:
                    insert_url_item(self.url_list,self.items)

                self.logger.info("URL has been seen before, stopping.")
                break
        
        
        response.request.headers['referer'] = response.url

        self.depth += 1
        if self.depth_stop():
            return

        if self.has_next_page:
            yield response.follow(self.start_urls[0].format(page=self.depth), self.parse,headers=response.request.headers,cookies=response.request.cookies,dont_filter=True)
 
    def depth_stop(self):

        if self.depth > 90:
            
            self.has_next_page = False
            insert_url_item(self.url_list,self.items)
            return True
        
        return False
    


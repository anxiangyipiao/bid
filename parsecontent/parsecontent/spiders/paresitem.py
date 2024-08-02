
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str
from ..util.mysql_manager import filter_words, keyword_value
from bs4 import BeautifulSoup
import re
from datetime import datetime

class ContentSpider(RedisSpider):
    
    name = "content"
    redis_key = 'content_items'
   

    def make_request_from_data(self, data):

        # 读取redis中的数据
        record = bytes_to_str(data, self.redis_encoding).split('|')
        
        url = record[0]
        # 如果标题中不包含任何过滤词，则请求
        if not self.filter_title(record[1]):
            metadata = {
                "title": record[1],
            }

            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "referer": 'https://zb.zhaobiao.cn'
            }


            return scrapy.Request(url=url,meta = metadata, callback=self.parse, method="GET", headers=header)
        

    def parse(self, response):
        
        title = response.meta["title"]
        url = response.url

        # 处理内容
        content = self.process_content(response.body)

        if not self.filter_content(content):
            return

        # 提取日期
        date = self.extract_data(content)

        # 返回数据
        yield {
            "url": url,
            "title": title,
            "date": date
        }


    def filter_title(self, title):
  
         # 如果标题中包含任何过滤词，则不请求
        if any(word in title for word in filter_words):
            return False
        
        return True
     
    def filter_content(self, content):
  
         # 如果标题中包含任何过滤词，则不请求
        if any(word in content for word in keyword_value):
            return True
        
        return False
    
    def process_content(self, content):
         # 使用BeautifulSoup解析html
        soup = BeautifulSoup(content, 'html.parser').body

        # 删除所有的<a>标签
        for a in soup.find_all('a'):
            a.decompose()

        # 获取所有的文本
        clean_text = soup.get_text()

        # 删除\n
        clean_text = clean_text.replace('\n', '').replace("*",'')

        return clean_text
    
    def extract_data(self, content):

        # 使用正则提取时间
        pattern = r'\b\d{4}-\d{2}-\d{2}\b'
        dates = re.findall(pattern, content)

        # 将所有找到的日期转换为 datetime 对象
        date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

        # 获取当前日期
        current_date = datetime.now()

        if not date_objects:

            return current_date.strftime('%Y-%m-%d')
        
        # 计算每个日期与当前日期之间的天数差，并找到最小差值的日期
        nearest_date = min(date_objects, key=lambda date: abs((date - current_date).days))

        return nearest_date.strftime('%Y-%m-%d')

    
        

            
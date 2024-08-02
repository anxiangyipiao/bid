from .redis_manager import redis_manager_urls, redis_manager_items
from fake_useragent import UserAgent
ua = UserAgent()


def extract_longest_link(quote):
    # 使用 XPath 选择器获取所有 <a> 标签的文本和链接
    a_texts = quote.xpath('.//a/text()').getall()
    a_links = quote.xpath('.//a/@href').getall()

    # 确保文本和链接的数量相同
    # assert len(a_texts) == len(a_links), "Number of texts and links do not match."

    # 找出文本最长的 <a> 标签
    max_length = 0
    longest_title = None
    longest_url = None

    for text, link in zip(a_texts, a_links):
        if len(text) > max_length:
            max_length = len(text)
            longest_title = text
            longest_url = link

    return longest_title, longest_url


def insert_url_item(url_list,items):

        # 更新增量爬取位置,redis是线程安全的，同一时间只有一个线程可以访问
        # 所以不用担心多线程问题，不会出现多个线程同时更新增量爬取位置
        redis_manager_urls.update_hash_seen(url_list[-1], url_list[0])
        # 删除最后一个重复的url,上次添加过
        del items[url_list[-1]]
        # 添加数据到redis items
        redis_manager_items.add_list_items(items)


def get_ua_headers():
    return {
        'User-Agent': ua.random,
    }
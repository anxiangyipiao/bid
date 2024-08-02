import redis
from redis import ConnectionPool
import json

class RedisManager:

    def __init__(self, host, port, db):
        # 创建连接池
        self.pool = ConnectionPool(host=host, port=port, db=db)
        # 初始化连接
        self.connect()

    def connect(self):
        """连接Redis"""
        # 从连接池中获取连接
        self.client = redis.Redis(connection_pool=self.pool)

    def close(self):
        """关闭Redis连接"""
        # 连接会被放回连接池而不是真正关闭
        self.client.connection_pool.disconnect()

    def has_hash_seen(self, url):
        """检查URL是否已经被访问过"""
        return self.client.hexists('urls_seen', url)

    def update_hash_seen(self, oldurl, newurl):
        """更新哈希中的URL"""
        # 必须先删除oldurl，再添加newurl，同时保证原子性
        # 使用pipeline可以保证原子性，即要么同时成功，要么同时失败
        pipe = self.client.pipeline()
        pipe.hdel('urls_seen', oldurl)
        pipe.hmset('urls_seen', {newurl: 1})
        pipe.execute()

    def add_hash_seen(self, url):
        """添加URL到哈希"""
        try:
            self.client.hset('urls_seen', url, 1)
        except redis.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")

    def add_list_items(self, items: dict):
    # 将字典中的每个键值对转换成字符串并分别存储到 Redis 列表中
        try:
            for key, value in items.items():
                # 使用 json.dumps 将键值对转化为字符串，这样可以处理不可直接转化为 str 的数据类型
                item_str = json.dumps({key: value})
                redis_manager_items.client.lpush('content_items', item_str)
        except redis.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        
 
# 全局redis_manager，初始化一个redis连接池
redis_manager_urls = RedisManager('localhost', 6379, 0)

# 批量插入未过滤的数据
redis_manager_items = RedisManager('localhost', 6379, 1)





if __name__ == '__main__':
#     # 测试
#     redis_manager = RedisManager('localhost', 6379, 0)

    # 测试添加URL
    # redis_manager_urls.add_hash_seen('https://www.qianlima.com/bid-435889739.html')
    
    pass
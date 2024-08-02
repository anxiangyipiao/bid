import pymysql


class MysqlManager:

    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def execute(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def fetch_all(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def fetch_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetch_many(self, sql, size):
        self.cursor.execute(sql)
        return self.cursor.fetchmany(size)

    def fetch_urls(self):
        return self.fetch_all("select id,source,root_url,bid_url_prefix,list_xpath,url_xpath,title_xpath,time_xpath from url_params_more where id = 2")        
    

# mysql:
#   # host: 10.4.200.196
#   host: 127.0.0.1
#   port: 3306
#   user: root
#   db: bidSpider2
#   password: "123456"
#   # password: cSFbhtFencqH3knm
#   table: bid_info
#   charset: utf8mb4

# 将mysql数据插入到redis中


mysql_manager = MysqlManager(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="123456",
    db="bidSpider2",
    )

# mysql_manager.connect()

# url = mysql_manager.fetch_urls()

# mysql_manager.close()

# # 链接redis

# redis_manager = RedisManager()

# redis_manager.connect()


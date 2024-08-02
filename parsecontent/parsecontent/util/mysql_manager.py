import pymysql

# 使用线程池，避免频繁创建和销毁连接
class MysqlManager:

    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            charset="utf8mb4"
        )
        self.cursor = self.conn.cursor()
   
    # 查询过滤关键词
    def query_filter_keyword(self):
        sql = "select distinct(filter_value) from filter_words"
        self.cursor.execute(sql)
        words_list = self.cursor.fetchall()
        words_list = [d[0] for d in words_list]
        return words_list

    def query_keyword(self):
        sql = "select keyword_parameter_value from keyword_value where avail_status = 1"
        self.cursor.execute(sql)
        words_list = self.cursor.fetchall()
        words_list = [d[0] for d in words_list]
        return words_list

# mysql:
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

filter_words = mysql_manager.query_filter_keyword()

keyword_value = mysql_manager.query_keyword()



# -*-coding:utf-8 -*-
import sqlite3


class DataBaseHelper:
    def __init__(self):
        # 打开数据库连接
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    # 执行sql语句
    def execute(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    # 批量执行sql语句
    def batch_execute(self, sql_list):
        for sql in sql_list:
            self.cursor.execute(sql)
        sql.conn.commit()

    # 关闭数据库
    def close(self):
        self.conn.close()

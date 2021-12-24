# -*- coding: UTF-8 -*-
"""
@Project : 4-前程无忧-scrapy-mysql 
@File    : Jobs51Database.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 14/09/2021 15:14 
@Brief   : 
"""
from typing import Dict, List
import pymysql


class JobsDatabase:
    def __init__(self, database: str, host: str = '127.0.0.1', port: int = 3306, user: str = 'root',
                 password: str = '123456'):
        self.connection = pymysql.Connection(
            user=user, host=host, port=port, password=password, database=database
        )
        self.cursor = self.connection.cursor()

    def all(self):
        """Print all information of this dataset."""
        sql = 'select * from jobs51;'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert(self, data_list: List[Dict]):
        """Inset into information."""
        sql = 'insert into jobs51(JobName, CompanyName, WorkingArea, Salary) value (%s,%s,%s,%s);'
        for index, data in enumerate(data_list):
            try:
                self.cursor.execute(sql, [data['JobName'], data['CompanyName'], data['WorkingArea'], data['Salary']])
                # 每10条保存一次
                if (index + 1) % 10 == 0:
                    self.connection.commit()

            except:
                print(f"JobName: {data['JobName']}, CompanyName: {data['CompanyName']}, WorkingArea: {data['WorkingArea']}, Salary: {data['Salary']} went wrong when writing into the SQL")
                # self.connection.rollback()
        if len(data) % 10:
            self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    db = JobsDatabase('python')
    data = {'JobName': '售后数据分析主管', 'CompanyName': '广东九极生物科技有限公司', 'WorkingArea': '广州-天河区', 'Salary': '6-8千/月'}
    db.insert([data])
    db.close()

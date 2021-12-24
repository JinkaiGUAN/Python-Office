# -*- coding: UTF-8 -*-
"""
@Project : 4-前程无忧-scrapy-mysql 
@File    : spider.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 14/09/2021 10:33 
@Brief   : 
"""
import random
import time
from typing import List, Dict

import csv
import json
import os.path
import re
from urllib.parse import quote

import requests

from database.Jobs51Database import JobsDatabase

db = JobsDatabase('python')


class Job51Spider:
    """爬取对应栏目前五页文章。"""

    def __init__(self, career_name: str = '数据分析', page_nums: int = 5, save_method: str = 'csv'):
        self.career_name = career_name
        self.page_nums = page_nums
        self.save_method = save_method

        self.url_format = 'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html'
        self.headers = {
            'Host': 'search.51job.com',
            'Referer': 'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,1.html'.format(quote('数据分析')),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        }

        self.file_path = self.clear_file('jobs51-{}.csv'.format(self.career_name))
        self.file = open(self.file_path, mode='a', encoding='gbk', newline='')
        self.csv_writer = csv.DictWriter(self.file, fieldnames=['JobName', 'CompanyName', 'WorkingArea', 'Salary'])
        self.csv_writer.writeheader()

    def clear_file(self, filename: str = 'jobs41.csv'):
        current_path = os.path.abspath(os.path.join(os.getcwd(), filename))
        with open(current_path, mode='w', encoding='gbk', newline='') as f:
            f.truncate(0)

        return current_path

    def save(self, data_list: List[Dict]):
        self.csv_writer.writerows(data_list)

    def parse_single_apge(self, url: str, headers: Dict):
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(1 + random.random())
        data_info = re.findall("""window.__SEARCH_RESULT__ = \{(.*)\}</script>""", response.text, re.S)
        # 反序列化
        json_data = json.loads("{" + data_info[0] + "}")
        data_list = json_data['engine_jds']
        datas = []
        for data in data_list:
            job_name = data['job_name']
            company_name = data['company_name']
            working_place = data['workarea_text']
            salary = data['providesalary_text']
            datas.append({
                'JobName': job_name, 'CompanyName': company_name, 'WorkingArea': working_place, 'Salary': salary})
            # print(f'JobName: {job_name}, CompanyName: {company_name}, WorkingArea: {working_place}, Salary: {salary}')

        return datas

    def update_request_info(self, page_num: int):
        url = self.url_format.format(self.career_name, page_num)
        referer = self.url_format.format(quote(self.career_name), page_num)
        self.headers['Referer'] = referer

        return url, self.headers

    def run(self):
        for page_num in range(1, self.page_nums + 1):
            url, headers = self.update_request_info(page_num)
            data = self.parse_single_apge(url, headers)
            self.save(data)
            if self.save_method == 'sql':
                db.insert(data)
        self.file.close()

    def __enter__(self):
        """进入上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        print('<------------- Job {} Finished ------------->'.format(self.career_name))
        print('Exec_type: ', exc_type)
        print('Exec_value: ', exc_val)
        print('Exec_tb: ', exc_tb)


def main():
    """获取数据分析、数据挖掘、算法、机器学习、深度学习、人工智能相关信息。"""
    names = ["数据分析", "数据挖掘", "算法", "机器学习", "深度学习", "人工智能"]

    for name in names:
        with Job51Spider(career_name=name) as job:
            job.run()
        # break


if __name__ == '__main__':
    # job51 = Job51Spider()
    # job51.run()
    main()

    db.close()

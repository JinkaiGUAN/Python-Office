# -*- coding: UTF-8 -*-
"""
@Project : 4-前程无忧-scrapy-mysql 
@File    : spider.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 14/09/2021 20:47 
@Brief   : 
"""
from typing import List

import csv
import os.path
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class SeleniumSpider:
    def __init__(self, career_name: str = '数据分析', page_nums: int = 5, save_method: str = 'csv',
                 executable_path: str = './chromedriver.exe'):
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        self.career_name = career_name
        self.page_nums = page_nums

        self.driver = webdriver.Chrome(executable_path=executable_path)#, options=chrome_options)
        self.url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,1.html'.format(career_name)

        self.current_dir = self.create_data_folder()
        filename = self.clear_scv_file('jobs51-{}.csv')
        self.file = open(filename, mode='a', encoding='gbk', newline='')
        self.csv_writer = csv.DictWriter(self.file, fieldnames=['JobName', 'CompanyName', 'WorkingArea', 'Salary'])
        self.csv_writer.writeheader()

    def clear_scv_file(self, filename='jobs51-{}.csv'):
        filename = os.path.join(self.current_dir, filename.format(self.career_name))
        with open(filename, mode='w', encoding='gbk', newline='') as f:
            f.truncate(0)

        return filename

    def create_data_folder(self):
        current_dir = os.path.abspath(os.path.join(os.getcwd(), 'data'))
        if not os.path.exists(current_dir):
            os.mkdir(current_dir)
        return current_dir

    def parse_single_page(self):
        div_eles = self.driver.find_elements_by_css_selector('.j_joblist > div')
        datas = []
        for div_ele in div_eles:
            job_name = div_ele.find_element_by_css_selector('.t .jname.at').text
            company_name = div_ele.find_element_by_css_selector(' .er .cname.at').text
            working_place = div_ele.find_element_by_css_selector('.info .d.at').text.split('|')[0].strip()
            salary = div_ele.find_element_by_css_selector('.info .sal').text
            datas.append({
                'JobName': job_name, 'CompanyName': company_name, 'WorkingArea': working_place, 'Salary': salary})

        return datas

    def scroll_page(self):
        for h in range(1, 11, 2):
            time.sleep(0.5)
            j = h / 9
            js_all = 'document.documentElement.scrollTop=document.documentElement.scrollHeight * {:.1f}'.format(j)
            self.driver.execute_script(js_all)

    def save_data(self, datas: List):
        self.csv_writer.writerows(datas)

    def run(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        for page_num in range(1, self.page_nums + 1):
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                'body > div:nth-child(4) > div.j_result > div > div.j_tlc > div.tleft > span.ss.on'))
            )

            self.scroll_page()
            datas = self.parse_single_page()
            print(datas)
            self.save_data(datas)

            # 下一页
            if page_num < self.page_nums:
                next_page_btn = self.driver.find_element_by_css_selector(
                    'body > div:nth-child(4) > div.j_result > div > div.leftbox > div:nth-child(4) > div.j_page > div > div > div > ul > li.next')
                next_page_btn.click()  # <div class="bbox">...</div>
            break
        input()
        self.driver.quit()
        self.file.close()


if __name__ == '__main__':
    selenium_jobs = SeleniumSpider()
    selenium_jobs.run()

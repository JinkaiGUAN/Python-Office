# -*- coding: UTF-8 -*-
"""
@Project : SimpleProject 
@File    : ip_filter.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 13/08/2021 09:13 
@Brief   : 
"""
import os


class IPFilter:
    def __init__(self):
        self.original_txt_path = os.path.abspath(os.path.join(os.getcwd(), 'ip.txt'))
        self.filter_txt_path = os.path.abspath(os.path.join(os.getcwd(), 'filted_ip.txt'))

    def filter_content(self):
        # clear the file
        with open(self.filter_txt_path, 'a+', encoding='utf-8') as test:
            test.truncate(0)

        with open(self.original_txt_path, 'r', encoding='utf-8-sig', newline='\n') as old_ip:
            with open(self.filter_txt_path, 'w', encoding='utf-8-sig', newline='\n') as new_ip:
                for line in old_ip:
                    ip = line.split('\t')[0]
                    time = float(line.split("\t")[1][:-1]) if line.split("\t")[1][:-1] else 3.0
                    # position = line.split('\t')[2]
                    if time < 1.0:
                        new_ip.write(ip)
                        new_ip.write('\n')

    def exec(self):
        self.filter_content()



if __name__ == "__main__":
    filter = IPFilter()
    filter.exec()


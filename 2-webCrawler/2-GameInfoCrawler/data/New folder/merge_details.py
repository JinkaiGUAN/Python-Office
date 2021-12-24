# -*- coding: UTF-8 -*-
"""
@Project : 2-GameInfoCrawler 
@File    : merge_details.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 01/09/2021 20:27 
@Brief   : 
"""
import os
import csv


class MergeDetails:
    def __init__(self):
        self.keys = [
                'GameName','EnglishName',
                    'SupportPlatforms','Developer','Publisher','pc','ChineseVersion1',
                    'ps4','ChineseVersion2','ps5','ChineseVersion3','xbox one','ChineseVersion4',
                    'xbox serious','ChineseVersion5','switch','ChineseVersion6','3ds',
                    'ChineseVersion7','psv','ChineseVersion8'
                ]

        self.total_detail_csv_path = os.path.abspath(os.path.join(os.getcwd(), 'finalData.csv'))
        self.total_detail_csv_file = open(self.total_detail_csv_path, mode='a', encoding='utf-8-sig', newline='\n')
        self.clear_total_data()
        self.csv_writer = csv.DictWriter(self.total_detail_csv_file, fieldnames=self.keys)
        self.csv_writer.writeheader()

    def clear_total_data(self):
        self.total_detail_csv_file.truncate(0)

    def open_total_details(self): pass

    def run(self):
        csv_path_list = ['1-details.csv', '2-details.csv']
        for csv_path in csv_path_list:
            with open(os.path.abspath(os.path.join(os.getcwd(), csv_path)), mode='r', encoding='utf-8-sig', newline='\n') as f:
                csv_reader = csv.DictReader(f)

                for row in csv_reader:
                    self.csv_writer.writerow(row)
                    print(row)

        self.total_detail_csv_file.close()

if __name__ == "__main__":
    merge_data = MergeDetails()
    merge_data.run()
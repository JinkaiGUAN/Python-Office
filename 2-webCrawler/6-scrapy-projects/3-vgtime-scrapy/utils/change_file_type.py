# -*- coding: UTF-8 -*-
"""
@Project : 8-vgtime-scrapy 
@File    : change_file_type.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 10/09/2021 10:33 
@Brief   : 
"""
import os.path

import pandas as pd


def move_excel2csv(excel_file_path: str, csv_file_name: str):
    data = pd.read_excel(excel_file_path)
    data.to_csv(os.path.abspath(os.path.join(os.path.dirname(excel_file_path), csv_file_name)), encoding='utf-8', index=False)


if __name__ == '__main__':
    excel_file_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'input_files', 'gamelist20210830.xlsx'))
    csv_name = 'GameNameList.csv'
    move_excel2csv(excel_file_path, csv_name)


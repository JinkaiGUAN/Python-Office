# -*- coding: UTF-8 -*-
"""
@Project : 4-vgtime 
@File    : step2_change_anchor_name.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 04/09/2021 11:46 
@Brief   : 
"""
from typing import List

import pandas as pd
import os
from tqdm import tqdm


def generate_anchor_file_paths(anchor_file_names: List):
    """生成主播表path"""
    return [os.path.abspath(os.path.join(os.getcwd(), '..', 'input_files', anchor_file_name)) for anchor_file_name
            in anchor_file_names]


def generate_target_anchor_file_paths(anchor_file_names: List):
    """生成主播表 csv file paths"""
    return [os.path.abspath(os.path.join(os.getcwd(), '..', 'input_files', anchor_file_name.split('.')[0] + '.csv')) for anchor_file_name
            in anchor_file_names]


def transfer_type_from_excel2csv(excel_file_path, csv_file_path):
    """转换表类型， from excel to csv"""
    data = pd.read_excel(excel_file_path)
    data.to_csv(csv_file_path, encoding='utf-8-sig', index=False)


class TransferNames:
    def __init__(self, anchor_file_names: List, new_username_file: List):
        self.anchor_file_paths = generate_anchor_file_paths(anchor_file_names)
        self.target_anchor_csv_paths = generate_target_anchor_file_paths(anchor_file_names)
        # 新用户表单只有一个
        self.new_username_file_path = generate_anchor_file_paths(new_username_file)[0]
        self.new_username_csv_file_path = generate_target_anchor_file_paths(new_username_file)[0]

    def merge_data2mapping(self):
        """制作总表， 得到映射链表. 总表名称固定"""
        total_csv_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'input_files',  'TotalAnchors.csv'))
        data = pd.read_csv(self.target_anchor_csv_paths[0])
        data.to_csv(total_csv_path,  encoding="utf-8-sig",index=False)

        for csv_path in self.target_anchor_csv_paths[1:]:
            data = pd.read_csv(csv_path)
            data.to_csv(total_csv_path,  encoding="utf-8-sig", index=False, mode='a+', header=False)

        # 读取总表id数据
        total_anchors_data = pd.read_csv(total_csv_path)
        total_userIds = total_anchors_data['userID'].unique()

        #得到新用户数据
        transfer_type_from_excel2csv(self.new_username_file_path, self.new_username_csv_file_path)
        new_username_data = pd.read_csv(self.new_username_csv_file_path)
        new_username = new_username_data['用户名']

        # 建立映射
        mapping_name = {anchor_name: new_user_name for anchor_name, new_user_name in
            zip(total_userIds, new_username[:len(total_userIds)])}

        return mapping_name

    def update_userId(self):
        for index, csv_path in enumerate(self.target_anchor_csv_paths):
            print('Update userId for file {}'.format(index + 1))

            A1_anchor = pd.read_csv(csv_path)
            for row_index, name in tqdm(zip(A1_anchor.index, A1_anchor['userID'])):
                new_name = self.mapping_name[name]
                A1_anchor.loc[row_index, 'userID'] = new_name
            A1_anchor.to_csv(csv_path, encoding="utf-8-sig", index=False)

    def run(self):
        # 1. 转换表类型， from excel to csv
        for anchor_file_path, target_anchor_csv_path in zip(self.anchor_file_paths, self.target_anchor_csv_paths):
            transfer_type_from_excel2csv(anchor_file_path, target_anchor_csv_path)

        # 2. 制作总表， 得到映射链表
        self.mapping_name = self.merge_data2mapping()

        # 3. 替换userId
        self.update_userId()


if __name__ == "__main__":
    anchor_file_names = [
        'A1_主播表.xlsx',
        'B1_主播表.xlsx',
        'C1_主播表.xlsx',
    ]
    new_usernames_file = ['新用户名表.xlsx']

    transfer_names = TransferNames(anchor_file_names, new_usernames_file)
    transfer_names.run()
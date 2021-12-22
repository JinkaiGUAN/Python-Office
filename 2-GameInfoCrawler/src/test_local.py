# -*- coding: UTF-8 -*-
"""
@Project : 2-GameInfoCrawler 
@File    : test_local.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 01/09/2021 17:49 
@Brief   : 
"""
import copy

if __name__ == "__main__":
    brand_list = [('pc', 'ChineseVersion1'),
                  ('ps4', 'ChineseVersion2'), ('ps5', 'ChineseVersion3'), ('xbox one', 'ChineseVersion4'),
                  ('xbox serious', 'ChineseVersion5'), ('switch', 'ChineseVersion6'), ('3ds',
                                                                                       'ChineseVersion7'),
                  ('psv', 'ChineseVersion8')]

    data = {'ChineseName': '这个'}

    platform_list = [('PS5', 'false'), ('XLSX', 'true'), ('PS6', 'false'), ('PS4', 'true'), ('PC', 'true'), ('switch', 'true')]
    # release_time_list = ['1', '2', '3', '4', '5', '6']
    release_time_list = ['1']

    release_time_list = [release_time_list[0] for _ in range(len(platform_list))] if len(release_time_list) <= 1 else release_time_list[:-1]

    platform_string = ''

    for (platform_true, chinese_version_true), release_time in zip(platform_list, release_time_list):

        platform_string = platform_string + platform_true.lower() + ', '
        for brand, chinese_version in brand_list:
            if platform_true.lower() == brand:
                data[copy.deepcopy(brand)] = copy.deepcopy(release_time)
                data[copy.deepcopy(chinese_version)] = copy.deepcopy(chinese_version_true)

        for brand, chinese_version in brand_list:
            if brand not in data.keys():
                data[brand] = ''
                data[chinese_version] = ''


    print(data)
    print(len(data))
    print(platform_string)

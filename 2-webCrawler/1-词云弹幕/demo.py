# -*- coding: UTF-8 -*-
"""
@Project : 1-词云弹幕 
@File    : demo.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 28/08/2021 22:01 
@Brief   : 
"""
import re
import os

import requests
from requests.utils import get_encodings_from_content
import jieba
import wordcloud
import imageio


class WordCloudAnalysis:
    def __init__(self):
        self.url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=383545816'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        self.filename = './data.txt'
        self.background_pic_path ='./zhuque.svg'

    def parse_url(self, url, times=5):
        try:
            response = requests.get(url, headers=self.headers, timeout=(7, 7))
            if response.encoding == 'ISO-8859-1':
                meta_encodings = get_encodings_from_content(response.text)
                if meta_encodings:
                    encoding = meta_encodings[0]
                else:
                    encoding = response.apparent_encoding
            else:
                encoding = response.encoding
            response.encoding = encoding

            return response.text

        except Exception as e:
            print(e)
            if times >= 1:
                self.parse_url(url, times - 1)
            else:
                return None

    def save_data(self, text):
        data_list = re.findall("<d p=.*?>(.*?)</d>", text, re.S)
        with open(self.filename, mode='w', encoding='utf-8') as f:
            for data in data_list:
                f.write(data + '\n')

    def seg_words(self):
        with open(self.filename, mode='r', encoding='utf-8') as f:
            text = f.read()
            text_list = jieba.lcut(text)
            return ' '.join(text_list)

    def output_wordcloud_pic(self, string):
        pic = imageio.imread(self.background_pic_path)
        wc = wordcloud.WordCloud(
            width=800,  # 宽度
            height=800,  # 高度
            background_color='white',  # 背景颜色
            font_path='msyh.ttc',  # 字体文件
            mask=pic,
            stopwords={'会', '飞过'},  # 停用词
        )
        wc.generate(string)
        wc.to_file('output.png')

    def run(self):
        if not os.path.exists(self.filename):
            html_text = self.parse_url(self.url, 5)
            self.save_data(html_text)
        else:
            string = self.seg_words()
            self.output_wordcloud_pic(string)


if __name__ == "__main__":
    word_cloud = WordCloudAnalysis()
    word_cloud.run()

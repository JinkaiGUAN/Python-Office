# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os.path

from itemadapter import ItemAdapter


class Jobs51Pipeline:
    def process_item(self, item, spider):
        return item


class CsvJobs51Pipeline:

    names = ["数据分析", "数据挖掘", "算法", "机器学习", "深度学习", "人工智能"]

    def __init__(self):
        self.mapping = {name: index for index, name in enumerate(self.names)}

        data_dir = self.create_data_dir()

        self.paths = [os.path.join(data_dir, 'jobs51-{}.csv'.format(name)) for name in self.names]
        self.clear_csv_data(self.paths)

        self.files, self.csv_writers = self.get_csv_writers()

    def get_csv_writers(self):
        files, csv_writers = [], []
        for path in self.paths:
            file = open(path, mode='a', encoding='gbk', newline='')
            csv_writer = csv.DictWriter(file, fieldnames=['JobName', 'CompanyName', 'WorkingArea', 'Salary'])
            csv_writer.writeheader()
            files.append(file)
            csv_writers.append(csv_writer)

        return files, csv_writers

    def create_data_dir(self):
        data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data'))
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        return data_dir

    def clear_csv_data(self, file_paths):
        for file_path in file_paths:
            with open(file_path, mode='w', encoding='gbk', newline='') as f:
                f.truncate(0)

    def process_item(self, item, spider):
        dict_ = dict(item)
        # postfix = dict_.pop('SearchName')
        index = self.mapping.get(dict_.pop('SearchName'))
        self.csv_writers[index].writerow(dict_)
        return item

    def close_spider(self, spider):
        [file.close() for file in self.files]

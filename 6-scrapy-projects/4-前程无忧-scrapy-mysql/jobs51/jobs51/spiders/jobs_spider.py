import json

import scrapy

from ..items import Jobs51Item


class JobsSpiderSpider(scrapy.Spider):
    name = 'jobs_spider'
    allowed_domains = ['51job.com']
    # start_urls = []
    url_format = 'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html'

    def start_requests(self):
        for search_name in ['数据分析', '数据挖掘', '算法', '机器学习', '深度学习', '人工智能']:
            # for search_name in ["数据挖掘"]:
            url = self.url_format.format(search_name, 1)
            yield scrapy.Request(url, callback=self.parse, meta={'PageNum': 1, 'SearchName': search_name})

    def parse(self, response):
        page_num = response.meta.get('PageNum')
        search_name = response.meta.get('SearchName')

        data_info = response.selector.re("""window.__SEARCH_RESULT__ = \{(.*)\}</script>""")
        # 反序列化
        json_data = json.loads("{" + data_info[0] + "}")
        data_list = json_data['engine_jds']
        for data in data_list:
            job_name = data['job_name']
            company_name = data['company_name']
            working_place = data['workarea_text']
            salary = data['providesalary_text']

            yield Jobs51Item(SearchName=search_name, JobName=job_name, CompanyName=company_name,
                             WorkingArea=working_place, Salary=salary)

        next_page = self.url_format.format(search_name, page_num + 1)
        if page_num <= 5:
            yield scrapy.Request(next_page, meta={'PageNum': page_num + 1, 'SearchName': search_name})

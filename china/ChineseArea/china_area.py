import pymysql
import requests
import lxml.etree as etree
import os


class ChineseArea(object):
    """获取省市区数据"""

    def __init__(self):
        """用户初始化数据库连接及定义存储数据的属性"""
        self.baseUrl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html'
        self.base = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/'
        self.chinses_data = {}
        # self.conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db="test", charset='utf8')
        self.levels = {
            1: '//tr[@class="provincetr"]',
            2: '//tr[@class="citytr"]',
            3: '//tr[@class="countytr"]',
            4: '//tr[@class="towntr"]',
            5: '//tr[@class="villagetr"]'
        }

    def get_province_data(self, url):
        """爬取行政区划代码公布页省级数据"""
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        i = 0
        while i < 3:
            try:
                html = requests.get(url, headers=headers, timeout=20)
                html.encoding = 'gbk'  # 这里添加一行
                text = html.text
                return text
            except requests.exceptions.RequestException:
                i += 1
                print('超时' + url)

    def parse_province(self):
        """解析省级数据，返回省列表数据"""
        html = self.get_province_data(self.baseUrl)
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='gbk'))
        nodes = tree.xpath('//tr[@class="provincetr"]')
        values = []
        for node in nodes:
            items = node.xpath('./td')
            for item in items:
                value = {}
                next_url = item.xpath('./a/@href')
                province = item.xpath('./a/text()')
                if province:
                    print(province)
                    value['url'] = self.base + "".join(next_url)
                    value['name'] = "".join(province)
                    value['code'] = "".join(next_url)[:2] + "0000000000"
                    value['pid'] = 0
                    value['level'] = 1
                    print(repr(value['name']))
                    last_id = self.insert_to_db(value)
                    value['id'] = last_id
                    values.append(value)
                    print(value)
        return values

    def parse_sub_data(self, level, pid, url):
        """根据级别解析子页数据"""
        if url.strip() == '':
            return None
        # url_prefix+url
        html = self.get_province_data(url)
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='gbk'))

        if level == 3:
            nodes = tree.xpath(self.levels.get(level))
            if len(nodes) == 0:
                nodes = tree.xpath(self.levels.get(4))
                print('有镇的市：' + url)
        else:
            nodes = tree.xpath(self.levels.get(level))

        path = os.path.basename(url)
        base_url = url.replace(path, '')
        values = []
        # 多个城市
        for node in nodes:
            value = {}
            next_url = node.xpath('./td[1]/a/@href')
            if len(next_url) == 0:
                next_url = ''
            code = node.xpath('./td[1]/a/text()')
            if len(code) == 0:
                code = node.xpath('./td[1]/text()')
            name = node.xpath('./td[2]/a/text()')
            if len(name) == 0:
                name = node.xpath('./td[2]/text()')
            value['code'] = "".join(code)
            temp_url = "".join(next_url)
            if len(temp_url) != 0:
                value['url'] = base_url + "".join(next_url)
            else:
                value['url'] = ''
            value['name'] = "".join(name)
            print(repr(value['name']))
            print(value['url'])
            value['pid'] = pid
            value['level'] = level
            last_id = self.insert_to_db(value)
            value['id'] = last_id
            values.append(value)
            print(value)
        return values

    def parse_villager(self, level, pid, url):
        """解析社区页数据"""
        html = self.get_province_data(url)
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='gbk'))
        nodes = tree.xpath(self.levels.get(level))
        values = []
        # 多个城市
        for node in nodes:
            value = {}
            nexturl = node.xpath('./td[1]/a/@href')
            code = node.xpath('./td[1]/text()')
            vcode = node.xpath('./td[2]/text()')
            name = node.xpath('./td[3]/text()')
            value['code'] = "".join(code)
            value['url'] = "".join(nexturl)
            value['name'] = "".join(name)
            print(repr(value['name']))
            value['pid'] = pid
            value['level'] = level
            values.append(value)
            last_id = self.insert_to_db(value)
            value['id'] = last_id
            values.append(value)
            print(value)
        return values

    def insert_to_db(self, value):
        """将数据保存到Mysql数据库中"""
        last_id = 0
        print(value)


    def parse_areas(self):
        """对外接口，用于获取所有省市区数据"""
        values = self.parse_province()
        for value in values:
            cities = self.parse_sub_data(2, value['id'], value['url'])
            if cities:
                for city in cities:
                    counties = self.parse_sub_data(3, city['id'], city['url'])


if __name__ == '__main__':
    """程序入口"""
    chinese_area = ChineseArea()
    chinese_area.parse_areas()

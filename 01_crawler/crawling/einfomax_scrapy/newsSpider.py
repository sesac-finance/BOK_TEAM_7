#  -*- coding: utf-8 -*-
 
import scrapy
import time
import csv
from newscrawling.items import NewscrawlingItem

class NewsSpider(scrapy.Spider):
    name = "newsCrawler"
    start_urls = []


    def start_requests(self):
        urls = []
        #5481
        for i in range(1,5481):
            urls.append("https://news.einfomax.co.kr/news/articleList.html?page={0}&total=164429&box_idxno=&sc_area=A&view_type=sm&sc_section_code=&sc_level=&sc_article_type=&sc_sdate=2012-11-21&sc_edate=2022-11-21&sc_order_by=E&sc_word=%EA%B8%88%EB%A6%AC&sc_andor=OR&sc_word2=".format(i))
        
        # pageNum = 2
        for url in urls:
            try:
                yield scrapy.Request(url=url, callback=self.parse, headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
            except:
                pass
        # sdate: 시작날짜 , edate : 끝 날짜

    def parse(self, response):
        urls = response.xpath('''//div[@class="list-block"]/div[@class="list-titles"]/a[contains(@href,list-titles)]/@href''').extract()
        
        for url in urls:
            url = 'http://news.einfomax.co.kr' + url
           
            yield scrapy.Request(url=url, callback=self.parse_details, headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
 
    def parse_details(self, response):
        item = NewscrawlingItem()
        item['date'] = response.xpath('// *[ @ id = "user-container"] / div[3] / header / section / div / ul / li[2] / text()').extract()
        item['title'] = response.xpath('//div[@class="article-head-title"]/text()').extract()
        item['article'] = response.xpath('//div[@id="article-view-content-div"]/text()').extract()
        item['url'] = response.url

        print('*'*100)
        print(item['url'])
        print(item['title'])
        return item


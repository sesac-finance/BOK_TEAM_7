#  -*- coding: utf-8 -*-
 
import scrapy
import time
import csv
from thebell.items import TheBellItem

class NewsSpider(scrapy.Spider):
    name = "thebellCrawler"
#16128

    def start_requests(self):
        urls = []
        for i in range(1,16130):
            urls.append("https://www.thebell.co.kr/free/content/article.asp?page={0}&svccode=00".format(i))
        
        # pageNum = 2
        for url in urls:
            try:
                print('url 성공')
                print(url)
                yield scrapy.Request(url=url, callback=self.parse, headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
            except:
                pass
        # sdate: 시작날짜 , edate : 끝 날짜

    def parse(self, response):
        urls = response.xpath('''//*[@id="contents"]/div[3]/div/div[1]/div[2]/div[2]/ul/li/dl/a/@href''').extract()
        print('parse 성공')
        print(urls)
        for url in urls:
            url = 'https://www.thebell.co.kr/free/content/'+url
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_details, headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})


    def parse_details(self, response):
        item = TheBellItem()
        item['date'] = response.xpath('//*[@id="contents"]/div[3]/div/div[1]/div/div[3]/div[1]/div[1]/span[2]/text()').extract()
        item['title'] = response.xpath('//*[@id="contents"]/div[3]/div/div[1]/div/div[3]/div[1]/p/text()').extract()
        item['article'] = response.xpath('//*[@id="article_main"]/text()').extract()
        item['url'] = response.url
        
        print('*'*100)
        print(item['date'])
        print(item['url'])
        print(item['title'])
        return item



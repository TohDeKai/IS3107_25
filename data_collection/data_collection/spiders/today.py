import datetime
import re

import requests
import scrapy
from scrapy.http import TextResponse


class TodaySpider(scrapy.Spider):
    name = "today"
    handle_httpstatus_list = [200]


    def start_requests(self):
        start_urls = ['https://www.todayonline.com/'] 
        for URL in start_urls:
            response = requests.get(URL)
            response = TextResponse(body=response.text, url=URL, encoding='utf-8')

            top_article = '//div[@class="card-object left-9s-6p__item"]'

            content = '//div[@class="list-object list-object--is-number"]'
            content = top_article + "|" + content
            content = response.xpath(content)
            category = re.findall('([^\/]*)', URL)[5]
            for article in content:
                article_url =  "https://www.todayonline.com/" + article.xpath('.//a//@href').get()
                
                yield (scrapy.Request(url=article_url, callback=self.parse_article, dont_filter=False,
                                    meta={'article_title': article_url, 'url': article_url, 'category' : category}))
            
    def make_blurp(self, text:str, limit=420):
        if text.startswith('Follow us on '):
            text = text.replace('Follow us on  Instagram  and  Tiktok , and join our  Telegram  channel for the latest updates. ','')
        if len(text) > limit:
            text = text[:limit]
        return text

    def parse_article(self, response):

        title = response.xpath('//h1[@class="h1 h1--page-title"]//text()').get()
        title = title.replace("\n","").strip()
        url = response.meta['url']

        category = response.meta['category']
        date = response.xpath('//div[@class="article-date article-date--"]//div[@class="article__row article__row--"]/text()').get()

        description = response.xpath('//meta[@property="og:description"]//@content').get()

        # processing date
        try:
            date = datetime.datetime.strptime(date, "%B %d, %Y")
        except:
            date = datetime.datetime.today()

        
        tags = response.xpath('//a[@class="link link--trending"]//text()').getall()
        for index in range(len(tags)):
            tags[index] = tags[index].replace("\n","").strip()

        yield {
            'title': title,
            'url': url ,
            'description': description,
            'date': date,
            'category': category,
            'keywords':tags,
            'source': self.name
            
        }
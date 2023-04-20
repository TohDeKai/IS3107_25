import scrapy
import re

class BBCSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['www.bbc.com']
    start_urls = ['https://www.bbc.com']

    def parse(self, response):
        articles =response.xpath('//div[@class="module__content"]//li')

        for article in articles:
            title = article.xpath('.//h3//a//text()').get()
            url = article.xpath('.//h3//a//@href').get()
            if url:
                yield response.follow(url=url, dont_filter=False,callback=self.parse_article, meta={ 'url': url, 'title': title})

    def parse_article(self,response):
        title = response.request.meta['title']
        url = response.request.meta['url']

        description = response.xpath('//meta[@name="description"]//@content').get()
        article_date = response.xpath('//time//@datetime').get()
        keywords = response.xpath('//meta[@type="metaTags"]//@content').getall()
        category = response.xpath('//meta[@property="article:section"]//@content').get()

        yield {
            'title': title,
            'url': url ,
            'description': description,
            'date': article_date,
            'category': category,
            'keywords':keywords,
            'source': self.name
        }
        

import scrapy
import re

class CNASpider(scrapy.Spider):
    name = 'cna'
    allowed_domains = ['www.channelnewsasia.com']
    start_urls = ['https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml']

    def parse(self, response):
        articles = response.xpath('//item')

        for article in articles:
            title = article.xpath('.//title//text()').get()
            url = article.xpath('.//link//text()').get()
            yield response.follow(url=url, dont_filter=False,callback=self.parse_article, meta={ 'url': url, 'title': title})

    def parse_article(self,response):
        title = response.request.meta['title']
        url = response.request.meta['url']

        description = response.xpath('//meta[@name="description"]//@content').get()
        article_date = response.xpath('//meta[@name="cXenseParse:recs:publishtime"]//@content').get()
        keywords = response.xpath('//meta[@name="keywords"]//@content').get()

        match = re.search(r"/([^/]+)/", url[1:])

        category = match.group(1)

        yield {
            'title': title,
            'url': url ,
            'description': description,
            'date': article_date,
            'category': category,
            'keywords':keywords,
            'source': self.name
        }
        

import json
import scrapy

class ASEANspider(scrapy.Spider):
    name = 'asean'
    allowed_domains = ['www.theaseanpost.com','theaseanpost.com']
    start_urls = ['https://theaseanpost.com/#'] 

    def parse(self, response):
        articles = response.xpath('//h3')

        for article in articles:
            url = article.xpath('.//a//@href').get()
            yield response.follow(url=url, dont_filter=False,callback=self.parse_article, meta={ 'url': url})

    def parse_article(self,response):
        title = response.xpath('//meta[@property="og:title"]//@content').get()
        url = response.request.meta['url']

        data = response.xpath('//script[@type="application/ld+json"]//text()').get()
        data = json.loads(data)
        description = data['@graph'][0]['description']
        article_date = data['@graph'][0]['datePublished']
        keywords = response.xpath('//meta[@name="keywords"]//@content').get()
        category = None

        yield {
            'title': title,
            'url': url ,
            'description': description,
            'date': article_date,
            'category': category,
            'keywords':keywords,
            'source': self.name
        }
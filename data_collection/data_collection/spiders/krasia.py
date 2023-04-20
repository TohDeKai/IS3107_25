import scrapy

class KrAsiaSpider(scrapy.Spider):
    name = 'krasia'
    allowed_domains = ['www.kr-asia.com','kr-asia.com']
    start_urls = ['https://console.kr-asia.com/feed'] # RSS Feed

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
        article_date = response.xpath('//meta[@property="article:published_time"]//@content').get()
        keywords = None
        category = response.xpath('//header//a//span//text()').get()

        yield {
            'title': title,
            'url': url ,
            'description': description,
            'date': article_date,
            'category': category,
            'keywords':keywords,
            'source': self.name,
            'region': "ASIA"
        }
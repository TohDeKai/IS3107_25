from cna import CNASpider
from krasia import KrAsiaSpider
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

def main():
    configure_logging()
    settings = get_project_settings()
    settings['FEED_URI'] = 'exports.json'
    settings['FEED_FORMAT'] = 'json'
    runner = CrawlerRunner(settings)  # from script, defaults provided
    runner.crawl(CNASpider) # your loop would go here
    runner.crawl(KrAsiaSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run() 


if __name__ == '__main__':
    main()
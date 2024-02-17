import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GtestSpiderSpider(CrawlSpider):
    name = "gtest_spider"
    allowed_domains = ["starwars.com"]
    start_urls = ["https://www.starwars.com/databank"]

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=('//li[@class="col item"]//a[contains(@class, "title-link")]',),
                allow=(),
                deny=('/video','/news'),
            ), 
            callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['response'] = response
        return item

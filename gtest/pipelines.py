# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GtestPipeline:
    def process_item(self, item, spider):
        x = ItemAdapter(item)
        r = item['response']
        x['url'] = r.url
        x['rich_text'] = r.xpath('//div[@class="rich-text-container"]//p/text()').getall()
        x['feature'] = r.xpath('//section[contains(@class, "featured_single")]//p/text()').getall()
        return item

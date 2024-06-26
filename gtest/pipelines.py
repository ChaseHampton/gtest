# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from collections.abc import Iterable
from scrapy.utils.response import open_in_browser
import re


class GtestPipeline:
    def process_item(self, item, spider):
        x = ItemAdapter(item)
        r = item['response']
        x['url'] = r.url
        x['rich_text'] = [x.strip() for x in r.xpath('//div[@class="rich-text-container"]//p//text()').getall() if x.strip()]
        x['feature'] = '\n'.join(r.xpath('//section[contains(@class, "featured_single")]//p/text()').getall())
        x["imgs"] = (
            r.xpath(
                '//section[contains(@class, "featured_single")]//img/@data-src'
            ).getall()
            + r.xpath('//section[contains(@class, "rich_text")]//img/@src').getall()
        )
        names = r.xpath(
            '//section[contains(@class, "featured_single")]//div[contains(@class, "content")]//*[contains(@class, "title")]//text()'
        ).getall()
        names = [x.strip() for x in names if x.strip()]
        name = names[0] if names else ""
        x["name"] = name
        x.pop('response')
        return x.asdict()

class GtestRichParse:
    def process_item(self, item, spider):
        x = ItemAdapter(item)
        if isinstance(x['rich_text'], Iterable):
            x['rich_text'] = ' '.join([x.strip() for x in x['rich_text'] if x.strip()])
        x['rich_text'] = re.sub(r'(?: (\W) | (\W)$)', lambda m: m.group()[1:], x['rich_text'])
        return x.asdict()

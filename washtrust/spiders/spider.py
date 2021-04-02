import scrapy

from scrapy.loader import ItemLoader

from ..items import WashtrustItem
from itemloaders.processors import TakeFirst


class WashtrustSpider(scrapy.Spider):
	name = 'washtrust'
	start_urls = ['https://www.washtrust.com/about/company-news']

	def parse(self, response):
		post_links = response.xpath('//ul[@class="insights-list"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[img[@alt="next page"]]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="content-head"]//h1/text()').get()
		description = response.xpath('//div[@class="full-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="date"]/text()').get()

		item = ItemLoader(item=WashtrustItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

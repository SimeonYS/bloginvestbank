import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import BloginvestbankItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class BloginvestbankSpider(scrapy.Spider):
	name = 'bloginvestbank'
	start_urls = ['https://ibank.bg/%d0%b1%d0%bb%d0%be%d0%b3/']

	def parse(self, response):
		post_links = response.xpath('//h1/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//span[@class="nav-prev"]/a/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)


	def parse_post(self, response):

		date = response.xpath('//h5/text()').get()
		title = response.xpath('//h1//text()').get()
		content = response.xpath('//span[@itemprop="articleBody"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=BloginvestbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()

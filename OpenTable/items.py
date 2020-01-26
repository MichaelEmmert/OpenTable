# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class OpentableItem(scrapy.Item):
	name = scrapy.Field()
	location = scrapy.Field()
	area = scrapy.Field()
	cuisine = scrapy.Field()
	review_count = scrapy.Field()
	review_link = scrapy.Field()
	link = scrapy.Field()
	cost = scrapy.Field()
	rating = scrapy.Field()
	promoted = scrapy.Field()
	location_on_page = scrapy.Field()
	bookings_today = scrapy.Field()
	address = scrapy.Field()
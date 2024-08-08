# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarItem(scrapy.Item):
    carUrl = scrapy.Field()
    carName= scrapy.Field()
    year = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    doors = scrapy.Field()
    color = scrapy.Field()
    style = scrapy.Field()
    price = scrapy.Field()
    lot = scrapy.Field()
    vinCode = scrapy.Field()
    description = scrapy.Field()
    carHL = scrapy.Field()
    views = scrapy.Field()

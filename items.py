# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst

class ScrapysongsItem(scrapy.Item):
    # define the fields for your item here like:
    band = scrapy.Field(output_processor=TakeFirst())
    song = scrapy.Field(output_processor=TakeFirst())

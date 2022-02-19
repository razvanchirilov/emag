# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# Extract data in this temporary containers -> items -> storing in database
import scrapy
from itemloaders.processors import TakeFirst


class EmagCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    product_description = scrapy.Field(output_processor=TakeFirst())
    product_reviews_no = scrapy.Field(output_processor=TakeFirst())
    product_rating = scrapy.Field(output_processor=TakeFirst())
    product_seller = scrapy.Field(output_processor=TakeFirst())
    product_price_PRP = scrapy.Field(output_processor=TakeFirst())
    product_price = scrapy.Field(output_processor=TakeFirst())
    product_specifications = scrapy.Field()



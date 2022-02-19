import scrapy
from itemloaders import ItemLoader
from scrapy.crawler import CrawlerProcess
from emag_crawler.emag_crawler.items import EmagCrawlerItem


class LaptopsSpider(scrapy.Spider):
    name = 'laptops'
    # next_page = 2
    start_urls = ['https://www.emag.ro/laptopuri/p1/c']

    def __init__(self):
        self.product_specifications = []
        self.product_price = []
        self.product_price_PRP = []

    def start_requests(self):
        yield scrapy.Request('https://www.emag.ro/laptopuri/p1/c', callback=self.parse)

    async def parse(self, response, **kwargs):
        # get the products container
        # products = response.css("div.js-products-container")
        products = response.css("div.card-item")
        # products = response.css("div.page-container")

        for product in products:
            # get the link for all the products
            link = product.xpath(".//div[@class='pad-hrz-xs']/a['href']/@href").get()

            # follow the links to get the info
            req = response.follow(url=link)

            # download the response async
            resp = await self.crawler.engine.download(req, self)

            # get the product xpath description
            product_description = resp.css("h1::text").get().strip()

            # get the product xpath reviews_no
            product_reviews_no = resp.xpath(".//a[@class='gtm_rp160118 dotted-link mrg-rgt-xxs']/text()").get()

            # get the product xpath rating
            product_rating = resp.xpath(
                ".//span[@class='star-rating-text gtm_rp101318 semibold text-gray-dark EOSMKP-90955-a']/text()").get()

            # get the product xpath seller
            product_seller = resp.xpath(".//div[@class='product-highlight highlight-vendor']/span/a/text()").get()

            # verify if the PRP is not NONE, get the product value for the RPR_price if it is available and append it to a variable,
            #  if not print the message
            if resp.xpath(
                ".//div[contains(@class, 'card-v2-content')]//span[contains(@class, 'rrp-lp30d-content')][1]/text()[1]"
            ):
                if resp.xpath(".//div[contains(@class, 'card-v2-content')]//span[contains(@class, 'rrp-lp30d-content')][1]/sup/text()[1]"):
                    product_PRP_raw = resp.xpath(
                ".//div[contains(@class, 'card-v2-content')]//span[contains(@class, 'rrp-lp30d-content')][1]/text()[1]"
                                    ).get().replace("PRP:", "").strip()
                    product_PRP_sup = resp.xpath(
                ".//div[contains(@class, 'card-v2-content')]//span[contains(@class, 'rrp-lp30d-content')][1]/sup/text()[1]"
                                    ).get()
                    product_PRP_price = [product_PRP_raw, product_PRP_sup]
                    self.product_price_PRP.append(".".join(product_PRP_price))
            else:
                print("produsul nu are PRP price")

            # verify if the price is not NONE,get the value for the product price,
            # if not print the message
            if resp.xpath(".//div[contains(@class, 'card-v2-content')]//p[contains(@class, 'product-new-price')]/text()[1]"):
                if resp.xpath(".//div[contains(@class, 'card-v2-content')]//p[contains(@class, 'product-new-price')]/sup/text()[1]"):
                    product_price_raw = resp.xpath(
                        ".//div[contains(@class, 'card-v2-content')]//p[contains(@class, 'product-new-price')]/text()[1]"
                                            ).get()
                    product_price_sup = resp.xpath(
                        ".//div[contains(@class, 'card-v2-content')]//p[contains(@class, 'product-new-price')]/sup/text()[1]"
                                                ).get()
                    product_price = [product_price_raw, product_price_sup]
                    self.product_price.append(".".join(product_price))
            else:
                print("produsul nu are pret")

            # get the table xpath response
            product_specifications_rows = resp.css('table.table.table-striped.product-page-specifications tr')

            # get the specs
            for specs in product_specifications_rows:
                specifications_column = specs.css('td::text')[0].get()
                specifications_value = specs.css('td::text')[1].get().strip()
                specs = [specifications_column, specifications_value]
                self.product_specifications.append(":".join(specs))

            # loader
            loader = ItemLoader(item=EmagCrawlerItem(), selector=product, response=response)
            loader.add_value("product_description", product_description)
            loader.add_value("product_reviews_no", product_reviews_no)
            loader.add_value("product_rating", product_rating)
            loader.add_value("product_seller", product_seller)
            loader.add_value("product_price_PRP", self.product_price_PRP)
            loader.add_value("product_price", self.product_price)
            loader.add_value("product_specifications", self.product_specifications)
            return loader.load_item()

        # next_page = 'https://www.emag.ro/laptopuri/p' + str(LaptopsSpider.next_page) + '/c'
        # if LaptopsSpider.next_page < 3:
        #     LaptopsSpider.next_page += 1
        #     yield response.follow(next_page, callback=self.parse)


# main driver #
if __name__ == "__main__":
    # Create instance called 'emag'
    emag = CrawlerProcess()
    emag.crawl(LaptopsSpider)
    emag.start()

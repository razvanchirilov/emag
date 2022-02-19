# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import mysql.connector


class LaptopsSpiderPipeline:
    def process_item(self, item, spider):
        return item

    # def __init__(self):
    #     self.create_connection()
    #     self.create_table()
    #
    # def create_connection(self):
    #     try:
    #         self.connection = mysql.connector.connect(
    #             host='localhost',
    #             user='root',
    #             passwd='@Chrazdan83!',
    #             database='sql_laptops'
    #         )
    #         print("Connection successfully")
    #     finally:
    #         print("Connection failed")
    #
    #     self.curr = self.connection.cursor()
    #
    # def create_table(self):
    #     self.curr.execute(""" DROP TABLE IF EXISTS laptops """)
    #     self.curr.execute(""" CREATE TABLE laptops
    #             (
    #             description text,
    #             availability text,
    #             price text,
    #             prp_price text
    #             )""")
    #
    # def process_item(self, item, spider):
    #     self.store_db(item)
    #     return item
    #
    # def store_db(self, item):
    #     self.curr.execute("""INSERT INTO laptops VALUES (%s, %s, %s, %s)""", (
    #         item['laptop_description'][0],
    #         item['availability'][0],
    #         ','.join(item['price']),
    #         ','.join(item['prp_price'])
    #
    #     ))
    #     self.connection.commit()
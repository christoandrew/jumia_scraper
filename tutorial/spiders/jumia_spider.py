import os
import random
import sqlite3

import scrapy


class JumiaSpider(scrapy.Spider):
    name = "jumia"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    start_urls = [
        "https://www.jumia.ug/electronics/",
        "https://www.jumia.ug/groceries/",
        "https://www.jumia.ug/health-beauty",
        "https://www.jumia.ug/baby-products",
        "https://www.jumia.ug/home-office",
        "https://www.jumia.ug/phones-tablets",
        "https://www.jumia.ug/computing",
    ]

    def __init__(self, name=None, **kwargs):
        super(JumiaSpider, self).__init__(name, **kwargs)
        self.conn = sqlite3.connect(
            "/Users/andrerw/PycharmProjects/tutorial/jumia/db.sqlite3"
        )
        self.cursor = self.conn.cursor()

    def parse(self, response):
        items = response.css("div.sku.-gallery")
        for item in items:
            sku = item.css("::attr(data-sku)").extract()
            if sku:
                sku = sku[0]

            title = item.css("h2.title").css("span.brand::text").get()
            name = item.css("h2.title").css("span.name::text").get()
            sku = sku if sku else None
            page = response.url
            position = items.index(item)
            discount = 0
            if item.css("span.sale-flag-percent::text").get():
                discount = int(item.css("span.sale-flag-percent::text").get()[:-1])
            discount_price = 0
            if item.css("span.price span::attr(data-price)").extract():
                discount_price = int(
                    item.css("span.price span::attr(data-price)").extract()[0]
                )
            price = 0
            if item.css("span.price.-old span::attr(data-price)").extract():
                price = int(item.css("span.price.-old span::attr(data-price)").extract()[0])

            source = "Unknown"
            if item.css("span.shop-logo span::attr(class)").extract():
                source = item.css("span.shop-logo span::attr(class)").extract()[0].split(" ")[1][1:]
            product = (
                random.randint(0000000, 9999999),
                title,
                name,
                discount,
                price,
                page,
                position,
                None,
                discount_price,
                response.url.split("/")[-2],
                source,
            )

            self.cursor.execute(
                "INSERT INTO web_product VALUES (?,?,?,?,?,?,?,?,?,?,?)", product
            )

            yield {
                "brand": item.css("h2.title").css("span.brand::text").get(),
                "name": item.css("h2.title").css("span.name::text").get(),
                "sku": sku if sku else None,
                "page": response.url,
                "position": items.index(item),
                "discount": item.css("span.sale-flag-percent::text").get(),
            }

            pagination = response.css("ul.osh-pagination")

            try:
                next_page = pagination.css("a[title='Next']::attr(href)").extract()[0]

                if next_page is not None:
                    yield response.follow(next_page, self.parse)
            except:
                pass
        self.conn.commit()

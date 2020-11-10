import scrapy
import sqlite3

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, name=None, **kwargs):
        super(QuotesSpider, self).__init__(name, **kwargs)
        self.conn = sqlite3.connect('jumia/db.sqlite3')
        self.cursor = self.conn.cursor()

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        quotes = response.css("div.quote")
        for quote in quotes:
            yield {
                "text": quote.css("span.text::text").get().strip(),
                "author": quote.css("small.author::text").get().strip(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

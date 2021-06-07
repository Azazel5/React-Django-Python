import csv
import scrapy
from scrapy.http import Request, request
from scrapy.loader import ItemLoader
from scrapy.item import Item, Field


class FromCSV(scrapy.Spider):
    name = 'fromcsv'

    def start_requests(self):
        with open("todo.csv") as file:
            reader = csv.DictReader(file)
            for line in reader:
                request = Request(line.pop('url'))
                request.meta['fields'] = line
                yield request

    def parse(self, response):
        item = Item()
        l = ItemLoader(item=item, response=response)
        for name, xpath in request.meta['fields'].iteritems():
            if xpath:
                item.fields[name] = Field()
                l.add_xpath(name, xpath)

        return l.load_item()

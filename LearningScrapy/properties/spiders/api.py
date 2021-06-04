import json
import scrapy
import datetime
import socket
from scrapy.http import Request
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from properties.items import PropertiesItem
from itemloaders.processors import MapCompose, Join


class ApiSpider(scrapy.Spider):
    name = 'api'

    start_urls = [
        'http://web:9312/properties/api.json',
    ]

    def parse(self, response):
        base_url = 'http://web:9312/properties/'
        js = json.loads(response.body)
        for item in js:
            id = item['id']
            title = item['title']
            url = base_url + "property_%06d.html" % id
            yield Request(url, meta={"title": title}, callback=self.parse_item)

    def parse_item(self, response):
        """ This function parses a property page.
        @url https://www.gumtree.com/p/property-to-rent/one-bedroom-property-near-chiswick-park-tube-station./1405437559
        @returns items 1
        @scrapes title price description address image_urls
        @scrapes url project server spider date
        """
        loader = ItemLoader(item=PropertiesItem(), response=response)

        loader.add_value('title', response.meta['title'], MapCompose(str.strip, str.title))
        
        loader.add_xpath(
            'price', '//h2[@itemprop="price"]/text()',
            MapCompose(lambda i: i.replace(',', ''), float), re='[,.0-9]+'
        )

        loader.add_xpath(
            'description', '//p[@itemprop="description"]/text()', MapCompose(str.strip), Join())
        loader.add_xpath(
            'address', '//h4[@itemprop="addressLocality"]/text()', MapCompose(str.strip))
        loader.add_xpath(
            'image_urls', '//*[@class="carousel-item"]/img/@src',
            MapCompose(lambda i: urljoin(response.url, i))
        )

        loader.add_value('url', response.url)
        loader.add_value('project', self.settings.get('BOT_NAME'))
        loader.add_value('spider', self.name)
        loader.add_value('server', socket.gethostname())
        loader.add_value('date', datetime.datetime.now())

        return loader.load_item()

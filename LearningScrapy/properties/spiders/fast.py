import scrapy
import datetime
import socket
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from properties.items import PropertiesItem
from itemloaders.processors import MapCompose, Join


class FastSpider(scrapy.Spider):
    name = 'fast'

    start_urls = [
        'https://www.gumtree.com/flats-houses/london'
    ]

    def parse(self, response):
        item_selector = response.xpath(
            '//*[@itemtype="http://schema.org/Product"]')
        yield from response.follow_all(item_selector, callback=self.parse_item)

        next_selector = response.xpath(
            '//li[@class="pagination-next"][1]/a/@href').extract()
        for selector in next_selector:
            yield response.follow(selector, callback=self.parse)

    def parse_item(self, response):
        """ This function parses a property page.
        @url https://www.gumtree.com/p/property-to-rent/one-bedroom-property-near-chiswick-park-tube-station./1405437559
        @returns items 1
        @scrapes title price description address image_urls
        @scrapes url project server spider date
        """
        loader = ItemLoader(item=PropertiesItem(), response=response)

        loader.add_xpath(
            'title', './/h1[@class="css-1uk1gs8 e1pt9h6u3"]/text()', MapCompose(str.strip))
        loader.add_xpath(
            'price', './/h2[@itemprop="price"]/text()',
            MapCompose(lambda i: i.replace(',', ''), float), re='[,.0-9]+'
        )

        loader.add_xpath(
            'description', './/p[@itemprop="description"]/text()', MapCompose(str.strip), Join())
        loader.add_xpath(
            'address', './/h4[@itemprop="addressLocality"]/text()', MapCompose(str.strip))
        loader.add_xpath(
            'image_urls', './/*[@class="carousel-item"]/img/@src',
            MapCompose(lambda i: urljoin(response.url, i))
        )

        loader.add_value('url', response.url)
        loader.add_value('project', self.settings.get('BOT_NAME'))
        loader.add_value('spider', self.name)
        loader.add_value('server', socket.gethostname())
        loader.add_value('date', datetime.datetime.now())

        return loader.load_item()

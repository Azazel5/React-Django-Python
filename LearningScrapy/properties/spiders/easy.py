import socket
import datetime
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from properties.items import PropertiesItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from itemloaders.processors import MapCompose, Join


class EasySpider(CrawlSpider):
    name = 'easy'
    # Start on the first index page
    start_urls = [
        'https://www.gumtree.com/flats-houses/london'
    ]

    # Rules for horizontal and vertical crawling
    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//*[@class="pagination-next"]/a')),
        Rule(LinkExtractor(restrict_xpaths='//*[@class="listing-link "]'),
             callback='parse_item')
    )

    def parse_item(self, response):
        """ This function parses a property page.
        @url http://web:9312/properties/property_000000.html
        @returns items 1
        @scrapes title price description address image_urls
        @scrapes url project spider server date
        """
        if not response:
            self.log("RESPONSE IS NONE")
        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('title', '//*[@itemprop="name"][1]/text()',
                    MapCompose(str.strip, str.title))
        l.add_xpath('price', './/*[@itemprop="price"][1]/text()',
                    MapCompose(lambda i: i.replace(',', ''), float),
                    re='[,.0-9]+')
        l.add_xpath('description', '//*[@itemprop="description"][1]/text()',
                    MapCompose(str.strip), Join())
        l.add_xpath('address',
                    '//*[@itemtype="http://schema.org/Place"][1]/text()',
                    MapCompose(str.strip))
        l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src',
                    MapCompose(lambda i: urljoin(response.url, i)))

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()

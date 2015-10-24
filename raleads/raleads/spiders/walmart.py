# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import urlparse
from decimal import Decimal
from w3lib.url import url_query_cleaner

from raleads.items import Product


class WalmartSpider(scrapy.Spider):
    name = "walmart"
    allowed_domains = ["www.walmart.com"]
    start_urls = (
        'http://www.walmart.com/',
    )

    def parse(self, response):
        # Get product details if /ip/ is in the URL
        if '/ip/' in response.url:
            # Remove the unnecessary parameters from the product url
            clean_url = url_query_cleaner(response.url)
            # Create a new Product
            p = Product()
            p['url'] = clean_url
            p['title'] = response.xpath("//h1[@itemprop='name']/span/text()").extract()[0].strip()
            price_data = response.xpath("//div[@itemprop='price']//text()").extract()

            if price_data:
                p['price'] = Decimal("".join(price_data[2:7]))
            else:
                p['price'] = Decimal("0")

            yield p

        # Check all of the links on the current page
        for link in response.xpath("//a/@href").extract():
            # Create an absolute url
            abs_url = urlparse.urljoin(response.url, link.strip())
            # Create a new request for a spider to crawl
            yield Request(url=abs_url)


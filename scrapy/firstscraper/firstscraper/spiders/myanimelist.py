# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MyanimelistSpider(CrawlSpider):
    name = 'myanimelist'
    allowed_domains = ['https://myanimelist.net']
    start_urls = ['https://myanimelist.net/topanime.php']

    rules = (
        Rule(LinkExtractor(allow=r'anime/'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item

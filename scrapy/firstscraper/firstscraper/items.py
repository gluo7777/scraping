# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Quote(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    page = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field(serializer=Author)


class Author(scrapy.Item):
    name = scrapy.Field()
    birthday = scrapy.Field()
    birthlocation = scrapy.Field()
    shortdescription = scrapy.Field()
    link = scrapy.Field()


class Anime(scrapy.Item):
    title = scrapy.Field()
    episodes = scrapy.Field(serializer=int)
    members = scrapy.Field(serializer=int)
    favorites = scrapy.Field(serializer=int)

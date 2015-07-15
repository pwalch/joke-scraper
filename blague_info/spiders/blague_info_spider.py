# To use the spider
# `scrapy crawl blague.info`

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from blague_info.items import BlagueInfoItem

import re

class BlagueInfoSpider(CrawlSpider):
    name = "blague.info"
    allowed_domains = ["www.blague.info"]
    start_urls = [
        "http://www.blague.info/blagues/administrations-23.html"
    ]

    rules = (
        Rule(LinkExtractor(
                restrict_xpaths=[
                    "//td/font[@color='#990000']/strong/a[starts-with(@href, 'http://www.blague.info/blagues/')]",
                    "//a[@class='lien' and starts-with(@href, '?')]"
                ]
            ),
            callback="parse_blague",
            follow=True
        ),
    )

    def parse_blague(self, response):
        jokeRowSelection = response.xpath("//a[starts-with(@href, 'humour/drole-')]/../../..")
        for jokeRow in jokeRowSelection:
            item = BlagueInfoItem()
            visitSectionSelection = jokeRow.xpath("./font[@class='visit']")
            item["title"] = visitSectionSelection.xpath("./font/a[@class='humour']/text()").extract()
            yield item

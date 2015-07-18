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
            callback="parse_joke_page",
            follow=True
        ),
    )

    @staticmethod
    def extract_joke(jokeRow, category):
        item = BlagueInfoItem()

        item["category"] = category

        visitSectionSelection = jokeRow.xpath("./font[@class='visit']")
        item["title"] = visitSectionSelection.xpath("./font/a[@class='humour']/text()").extract()[0]

        pointsDateText = visitSectionSelection.xpath("./text()[2]").extract()[0]
        pointsDateMatch = re.search("(\d+)\s*points[^\d]+([\d\/]+)", pointsDateText)
        item["points"] = int(pointsDateMatch.group(1))
        item["date_text"] = pointsDateMatch.group(2)

        item["content"] = "".join(jokeRow.xpath("./font[3]/node()").extract())

        return item

    def parse_joke_page(self, response):
        jokeRowSelection = response.xpath("//a[starts-with(@href, 'humour/drole-')]/../../..")

        category = re.search("blague - ([\w ]+) :", response.xpath("/html/head/title/text()").extract()[0]).group(1)
        for jokeRow in jokeRowSelection:
            yield BlagueInfoSpider.extract_joke(jokeRow, category)

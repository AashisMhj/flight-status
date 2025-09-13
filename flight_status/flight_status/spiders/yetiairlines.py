import scrapy


class YetiairlinesSpider(scrapy.Spider):
    name = "yetiairlines"
    allowed_domains = ["yetiairlines.com"]
    start_urls = ["https://yetiairlines.com/flight-status"]

    def parse(self, response):
        
        pass

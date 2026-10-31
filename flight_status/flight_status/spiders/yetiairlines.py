import scrapy


def clean(values):
    return " ".join(" ".join(values).split())


class YetiairlinesSpider(scrapy.Spider):
    name = "yetiairlines"
    allowed_domains = ["yetiairlines.com"]
    start_urls = ["https://yetiairlines.com/flight-status"]

    def parse(self, response):
        cards = response.css("article.landing-status-card")
        if not cards:
            self.logger.warning(f"No flight cards found on {response.url}, page layout may have changed")

        for card in cards:
            origin = card.css(".landing-status-card__airport:not(.landing-status-card__airport--to)")
            destination = card.css(".landing-status-card__airport--to")

            yield {
                "flight_no": clean(card.css(".landing-status-card__identity strong::text").getall()),
                "from_id": clean(origin.css(".landing-status-card__code::text").getall()),
                "to_id": clean(destination.css(".landing-status-card__code::text").getall()),
                "from": clean(origin.css(".landing-status-card__city::text").getall()),
                "to": clean(destination.css(".landing-status-card__city::text").getall()),
                "flight_time": clean(origin.css("strong::text").getall()),
                "arrival_time": clean(destination.css("strong::text").getall()),
                "revised_time": clean(card.css(".landing-status-card__journey small::text").getall()),
                "flight_status": clean(card.css(".landing-status-card__badge::text").getall()),
                "flight_remarks": clean(card.css(".landing-status-card__footer::text").getall()),
            }

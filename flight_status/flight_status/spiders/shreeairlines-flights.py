import scrapy
import json
from pathlib import Path


class ShreeairlinesSpider(scrapy.Spider):
    name = "shreeairlines"
    allowed_domains = ["www.shreeairlines.com"]
    start_urls = ["https://www.shreeairlines.com/flightstatus"]
    handle_httpstatus_list = [500]

    def start_requests(self):
        data_path = Path(__file__).parent / "shreeairlines-from-to.json"
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for departure in data['from']:
            for arrival in data[departure.get('fromValue')]:
                fromKey = departure.get('fromValue')
                toKey = arrival.get('value')
                if not fromKey == toKey :
                    yield scrapy.Request(f"https://www.shreeairlines.com/flightstatus?from={fromKey}&to={toKey}", callback=self.parse, cb_kwargs={"from_id": fromKey, "to_id": toKey, "departure": departure.get('fromLabel'), "arrival": arrival.get('label') }, meta={"dont_retry": True})
                    # check for return flights
                    yield scrapy.Request(f"https://www.shreeairlines.com/flightstatus?from={toKey}&to={fromKey}", callback=self.parse, cb_kwargs={"to_id": fromKey, "from_id": toKey, "arrival": departure.get('fromLabel'), "departure": arrival.get('label') }, meta={"dont_retry": True})
    def parse(self, response, from_id=None, to_id=None, arrival=None, departure=None):
        # the site's template crashes (500) for some routes, retrying doesn't help
        if response.status == 500:
            self.logger.warning(f"Server error for {from_id} -> {to_id}, skipping")
            return

        self.logger.info(f"Done: {from_id} -> {to_id}")
        rows = response.xpath("//table[contains(@class, 'table')]/tbody/tr[td]")
        for row in rows:
            yield {
                "flight_no": cell(row, 1),
                "from_id": from_id,
                "to_id": to_id,
                "departure": departure,
                "arrival": arrival,
                "sector": f"{cell(row, 2)} - {cell(row, 3)}",
                "flight_time": cell(row, 5),
                "revised_time": cell(row, 4),
                "flight_status": cell(row, 6),
                "flight_remarks": cell(row, 7)
            }


def cell(row, index):
    return " ".join(" ".join(row.xpath(f"./td[{index}]//text()").getall()).split())

import scrapy
import json
from pathlib import Path


class ShreeairlinesSpider(scrapy.Spider):
    name = "shreeairlines"
    allowed_domains = ["www.shreeairlines.com"]
    start_urls = ["https://www.shreeairlines.com/flightstatus"]

    def start_requests(self):
        data_path = Path(__file__).parent / "shreeairlines-from-to.json"
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for departure in data['from']:
            for arrival in data[departure.get('fromValue')]:
                fromKey = departure.get('fromValue')
                toKey = arrival.get('value')
                if not fromKey == toKey :
                    yield scrapy.Request(f"https://www.shreeairlines.com/flightstatus?from={fromKey}&to={toKey}", callback=self.parse, cb_kwargs={"from_id": fromKey, "to_id": toKey, "departure": departure.get('fromLabel'), "arrival": arrival.get('label') })
                    # check for return flights
                    yield scrapy.Request(f"https://www.shreeairlines.com/flightstatus?from={toKey}&to={fromKey}", callback=self.parse, cb_kwargs={"to_id": fromKey, "from_id": toKey, "arrival": departure.get('fromLabel'), "departure": arrival.get('label') }) 
    def parse(self, response, from_id=None, to_id=None, arrival=None, departure=None):
        self.logger.info(f"Done: {from_id} -> {to_id}")
        rows = response.xpath("//table[contains(@class, 'table-striped')]/tbody/tr")
        for row in rows:
            yield {
                "flight_no": row.xpath("./td[1]/text()").get(default="").strip(),
                "from_id": from_id,
                "to_id": to_id,
                "departure": departure,
                "arrival": arrival,
                "sector": row.xpath("./td[2]/text()").get(default="").strip(),
                "flight_time": row.xpath("./td[4]/text()").get(default="").strip(),
                "revised_time": row.xpath("./td[3]/text()").get(default="").strip(),
                "flight_status": row.xpath("./td[5]/text()").get(default="").strip(),
                "flight_remarks": row.xpath("./td[6]/text()").get(default="").strip()
            }

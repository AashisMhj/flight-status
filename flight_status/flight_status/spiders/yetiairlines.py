import scrapy
import json
from pathlib import Path
from datetime import datetime


class YetiairlinesSpider(scrapy.Spider):
    name = "yetiairlines"
    allowed_domains = ["yetiairlines.com"]
    start_urls = ["https://yetiairlines.com/flight-status"]

    def parse(self, response):
        code_path = Path(__file__).parent / "code.json"
        with open(code_path, "r", encoding="utf-8") as f:
            code = json.load(f)

        rows = response.xpath("//table[@id='flightInfo']/tbody/tr")

        for row in rows:
            departure = row.xpath("./td[1]/text()").get(default="").strip()
            arrival = row.xpath("./td[2]/text()").get(default="".strip())

            from_id = code.get(departure).get('code')
            to_id = code.get(arrival).get('code')

            yield {
                "flight_no": row.xpath("./td[3]/text()").get(default="").strip(),
                "from_id": from_id,
                "to_id": to_id,
                "from": departure,
                "to": arrival,
                "flight_time": row.xpath("./td[4]/text()").get(default="").strip(),
                "revised_time": row.xpath("./td[5]/text()").get(default="").strip(),
                "flight_status": row.xpath("./td[6]/text()").get(default="").strip(),
                "flight_remarks": row.xpath('./td[7]/text()').get(default="").strip()
            }
        

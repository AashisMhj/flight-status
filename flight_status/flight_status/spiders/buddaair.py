import scrapy
import json
from pathlib import Path
from datetime import datetime

class BuddaairSpider(scrapy.Spider):
    name = "buddaair"
    allowed_domains = ["www.buddhaair.com", "admin.buddhaair.com"]
    

    def start_requests(self, ):
        data_path = Path(__file__).parent.parent / "spiders/buddaair-from-to.json"
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for fromObj in data['from']:
            if fromObj.get('type') != 'single':
                fromKey = fromObj['fromValue']
                toObj = data[fromKey]
                for toValue in toObj:
                    self.logger.warning(f"https://admin.buddhaair.com/api/flight-status/{fromKey}/{toValue.get('toValue')}")
                    yield scrapy.Request(f"https://admin.buddhaair.com/api/flight-status/{fromKey}/{toValue.get('toValue')}", callback=self.parse, cb_kwargs={"from_id": fromKey, "to_id": toValue.get('toValue')})
    
    def parse(self, response, from_id=None, to_id=None):
        scraped_date_time = datetime.now()

        for item in response.xpath('//Flight'):
            self.logger.info(f"Done: {from_id} -> {to_id}")
            yield {
                "flight_no": item.xpath('FlightNo/text()').get(),
                "from_id": from_id,
                "to_id": to_id,
                "departure": item.xpath('Departure/text()').get(),
                "arrival": item.xpath('Arrival/text()').get(),
                "flight_time": item.xpath('FlightTime/text()').get(),
                "revised_time": item.xpath('RevisedTime/text()').get(),
                "flight_status": item.xpath('FlightStatus/text()').get(),
                "flight_remarks": item.xpath('FLightRemarks/text()').get()
            }

source .venv/bin/activate
cd flight_status/
scrapy crawl buddaair --loglevel=WARNING
scrapy crawl yetiairlines --loglevel=WARNING
scrapy crawl shreeairlines --loglevel=WARNING
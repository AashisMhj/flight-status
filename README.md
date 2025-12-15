# Flight Status
Scrape the flight data of Domestic flight of Nepali Airlines.

## Setup
```bash
## setup env
python3 -m venv .venv
# activate virtual environment
source .venv/bin/activate
```

There are multiple spiders in this project, each spider for a airline. You can run them individually or run all with the `scrape-flight.sh` script (Hope your are using linux 😬).
```bash
# run individual spider
scrapy crawl {{spider_name}} --loglevel=WARNING
```
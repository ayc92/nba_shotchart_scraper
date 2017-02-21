# nba_shotchart_scraper
Scrapes shotchart data into CSV files separated by player position.

First, you'll need to create a virtualenv and then install dependencies:
```
cd nba_shotchart_scraper
virtualenv venv
pip install -r requirements.txt
```

Now, to run the crawler, `cd` into the scrapy project root (the level of the directory containing the `scrapy.cfg` file, and then run `scrapy crawl shotchart`.

The output files will be in an `outputs/` directory at the scrapy project root.

BOT_NAME = 'shotchart_scraper'

SPIDER_MODULES = ['shotchart_scraper.spiders']
NEWSPIDER_MODULE = 'shotchart_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'shotchart_scraper.pipelines.ScraperPipeline': 300,
}

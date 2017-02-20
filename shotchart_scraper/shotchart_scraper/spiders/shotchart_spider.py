import simplejson as json

import scrapy

from shotchart_scraper.constants import TEAM_IDS
from shotchart_scraper.constants import TEAM_SHOTCHART_URL_FORMAT
from shotchart_scraper.items import create_item_class


def _get_team_shotchart_urls(team_ids, url_format):
    return [url_format.format(team_id=tid) for tid in team_ids]


class ShotchartSpider(scrapy.Spider):
    name = 'shotchart'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.shotchart_event_cls = None

    def start_requests(self):
        for url in _get_team_shotchart_urls(TEAM_IDS, TEAM_SHOTCHART_URL_FORMAT):
            yield scrapy.Request(url, callback=self.parse_shotchart_response)

    def parse_shotchart_response(self, response):
        response_json = json.loads(response.body_as_unicode())
        result_sets = response_json['resultSets'][0]
        headers = [h.lower() for h in result_sets['headers']]
        fields = list(headers)
        fields.append('player_position')
        if not self.shotchart_event_cls:
            self.shotchart_event_cls = create_item_class('ShotchartEventItem', fields)

        row_set = result_sets['rowSet']
        for row in row_set:
            row_dict = dict(zip(headers, row))
            yield self.shotchart_event_cls(**row_dict)

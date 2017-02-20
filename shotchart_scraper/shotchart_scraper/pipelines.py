from collections import namedtuple
import csv
import os
import requests
import simplejson as json

from scrapy.exceptions import DropItem


ACTIVE_PLAYERS_URL = 'http://www.nba.com/players/active_players.json'
OUTPUTS_DIR = 'outputs'


class PlayerWriter(namedtuple('PlayerWriter', ['fp', 'writer'])):
    @staticmethod
    def get_filepath(player_position):
        filename = '{}.csv'.format(player_position)
        cur_dir = os.path.dirname(__file__)
        return os.path.join(cur_dir, './{outputs_dir}/{filename}'.format(
            outputs_dir=OUTPUTS_DIR,
            filename=filename,
        ))

    @classmethod
    def from_item(cls, item):
        fp = open(cls.get_filepath(item['player_position']), 'w')
        writer = csv.DictWriter(fp, fieldnames=list(item.keys()))
        writer.writeheader()
        return cls(fp=fp, writer=writer)


class ScraperPipeline(object):
    def __init__(self):
        active_players_json = json.loads(requests.get(ACTIVE_PLAYERS_URL).content)
        self.active_players = {
            int(player['personId']): player
            for player in active_players_json
        }
        self.player_writers_map = {}

    def process_item(self, item, spider):
        player_id = int(item['player_id'])
        player = self.active_players.get(player_id)
        if not player:
            print('GOT HERE')
            raise DropItem('Player {} is no longer active.'.format(player_id))

        position = player['pos']
        item['player_position'] = position
        player_writer = self.player_writers_map.get(position)
        if not player_writer:
            self.player_writers_map[position] = PlayerWriter.from_item(item)

        player_writer.writer.writerow(dict(item))
        return item

    def close_spider(self, spider):
        for _, player_writer in self.player_writers_map.items():
            player_writer.fp.close()

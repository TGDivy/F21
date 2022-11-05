from unittest import TestCase
from lib.poi import POI, get_poi
import time


# could be moved to a global test setup method
from service.cache import cache
from flask import Flask
app = Flask(__name__)
cache.init_app(app)


class Test(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cache.delete_memoized(get_poi)

    def test_get_poi(self):
        place = 'london'
        poi_settings = {
            'value': 'subway',
            'tag': 'station',
            'weight': 0.5,
            'cap': 3
        }

        poi = POI(poi_settings)
        result, poi_dataframe = poi.get_poi(place)
        self.assertFalse(poi_dataframe.empty)

    def test_results_are_cached(self):
        start = time.time()
        place = 'london'
        poi_settings = {
            'value': 'subway',
            'tag': 'station',
            'weight': 0.5,
            'cap': 3
        }

        poi = POI(poi_settings)
        result, poi_dataframe = poi.get_poi(place)
        end = time.time()
        self.assertTrue((start - end) < 1)
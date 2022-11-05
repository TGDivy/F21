from unittest import TestCase
from hexagons import get_hexagons_geojson

# sincs get_hexagons_geojson relies on caching in sub methods cache must be initialized in tests
from service.cache import cache
from flask import Flask
app = Flask(__name__)
cache.init_app(app)


class Test(TestCase):
    def test_get_hexagons_geojson(self):
        selected_pois = [
            {'value': 'pub',
             'tag': 'amenity',
             'weight': 0.3,
             'cap': 30,
             },
            {'value': 'subway',
             'tag': 'station',
             'weight': 0.7,
             'cap': 1,
             }
        ]
        place = 'London'
        hex_resolution = 9
        geojson = get_hexagons_geojson(place, hex_resolution, selected_pois)
        assert geojson.is_valid == True
        assert geojson.type == 'FeatureCollection'

import flask
from flask import Flask, jsonify, request
from flask_cors import CORS
from service.cache import cache
from hexagons import get_hexagons_geojson
from lib.poi import POI
from lib.locationapi import get_long_lat_from
from threading import Thread

import orjson

app = Flask(__name__)
CORS(app)
cache.init_app(app)


@app.post('/hexagons')
def get_hexagons():
    body = request.get_json()
    place = body['place'].lower() # to avoid caching same place different casing
    hex_resolution = body['hex_resolution']
    selected_pois = body['selected_pois']
    only_show_scored = body['only_show_scored']

    geo = get_hexagons_geojson(place, hex_resolution, selected_pois, only_show_scored)
    center = get_long_lat_from(place)

    response = {
        'center': {
            'latitude': center['lat'],
            'longitude': center['lon'],
            'zoom': 10
        },
        'geojson': geo
    }


    return orjson.dumps(response)


@app.get('/poi')
def get_poi():
    args = request.args
    place = args.get('place', type=str)

    poi_settings = {
        'value': args.get('value', type=str),
        'tag': args.get('tag', type=str),
        'weight': args.get('weight', type=int),
        'cap': args.get('cap', type=int)
    }

    poi = POI(poi_settings)
    result, poi_dataframe = poi.get_poi(place)
    df_geo = poi_dataframe.dropna(subset=['lat', 'lon'], axis=0, inplace=False)
    df_geo.reset_index(drop=True, inplace=True)
    df_without = df_geo.filter(['name', 'geometry'])
    import geopandas
    gdf = geopandas.GeoDataFrame(df_without)
    json_string = gdf.to_json()

    return json_string


from service.cache import cache
from lib.poi import POI, get_poi
from roads import hex_roads
from geopoi import ScorePoi
import pandas as pd
from geojson import Feature, Point, FeatureCollection, Polygon

import logging


@cache.memoize(timeout=0)
def get_hexagons(place, resolution):
    hex_place = hex_roads.hexRoads(place=place)
    hex_place.get_place_hex(h3_resolution=resolution)
    hexagons = hex_place.place_hexes
    return hexagons

@cache.memoize(timeout=0)
def get_scored_df_for(place, hex_resolution, poi_tag, poi_values):
    hexagons = get_hexagons(place, hex_resolution)
    results, place_poi_df = get_poi(place, poi_tag, poi_values)
    scoring_for_poi = ScorePoi(place_poi_df, k=200, d=500)
    hex_scores_for_poi = scoring_for_poi.score_poi(hexagons, poi_name=poi_values[0])
    return hex_scores_for_poi


@cache.memoize(timeout=0)
def get_hex_scores_for(place, hex_resolution, pois):
    logging.info(f'getting hex_scores({place})')
    hexagon_df = get_hexagons(place, hex_resolution)
    hexagon_df.reset_index(inplace=True)
    poi_dataframes = []
    logging.info(f'iterating {len(pois)} pois')
    for poi in pois:
        poi_dataframe = get_scored_df_for(place, hex_resolution, poi['tag'], [poi['value']])
        poi_dataframes.append(poi_dataframe)

    logging.info('merging poi scores dataframes')
    last_left = None
    for i in range(len(poi_dataframes) - 1):
        if last_left is None:
            left = poi_dataframes[i]
        else:
            left = last_left
        right = poi_dataframes[i + 1]
        poi_score_key: str = f'score_{pois[i + 1]["value"]}'
        hex_scores = pd.merge(left, right[['hex_id', poi_score_key]], on='hex_id')
        last_left = hex_scores
        print('scored')

    logging.info(f'calculating weights for {place}')
    magic_number = 0
    hex_scores['total_score'] = 0
    for poi in pois:
        poi_score_key: str = f'score_{poi["value"]}'
        hex_scores[poi_score_key].clip(magic_number, poi['cap'], inplace=True)
        hex_scores[poi_score_key] = hex_scores[poi_score_key] / hex_scores[poi_score_key].max()
        hex_scores['total_score'] += (hex_scores[poi_score_key] * poi['weight'])

    logging.info(f'completed hex_scores({place})')
    return hex_scores

def get_google_link(gdf):
    '''
    Uses the geometry column to calculate latitude and longitude and create a google maps link from it.

    Returns: Geo data frame with additional column containing the google link
    '''
    gdf["centroid"] = gdf['geometry'].centroid
    gdf.set_geometry("centroid", inplace=True)
    gdf.to_crs(4326, inplace=True)
    gdf["latitude"] = gdf["centroid"].y
    gdf["longitude"] = gdf["centroid"].x

    # gdf['google_link'] = gdf.apply(
    #     lambda x: f"https://www.google.com/maps/@{round(x['latitude'], 5)},{round(x['longitude'], 5)},14z",
    #     axis=1)
    return gdf

def hexagons_dataframe_to_geojson(df_hex, hex_id_field, geometry_field, value_field):
    list_features = []

    for i, row in df_hex.iterrows():
        feature = Feature(geometry=row[geometry_field],
                          id=row[hex_id_field],
                          properties={"value": row[value_field], "hex_id": row[hex_id_field]})
        list_features.append(feature)

    feat_collection = FeatureCollection(list_features)
    logging.info('converted df to geojson')
    return feat_collection

@cache.memoize(timeout=0)
def get_hexagons_geojson(place, hex_resolution, selected_pois, should_drop_zero_score_hexes=True):
    poi_settings_for_data_gen = []
    POIs = []
    for selected_poi in selected_pois:
        poi = POI(selected_poi)
        POIs.append(poi)
        # limit whats fed to data gen to limit cache key surface
        poi_settings_for_data_gen.append({
            "tag": poi.tag,
            "value": poi.value,
            "weight": poi.weight,
            "cap": poi.cap
        })

    hex_scores = get_hex_scores_for(place, hex_resolution, poi_settings_for_data_gen)
    if (should_drop_zero_score_hexes):
        hex_scores.drop(hex_scores.index[hex_scores['total_score'] == 0.00000], inplace=True)
    hex_scores = get_google_link(hex_scores)
    geojson = hexagons_dataframe_to_geojson(hex_scores, 'hex_id', 'geometry', 'total_score')
    return geojson
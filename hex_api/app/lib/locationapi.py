import requests
from service.cache import cache

@cache.memoize(timeout=0)
def get_long_lat_from(text_search):
    api_url_for_search = "https://nominatim.openstreetmap.org/search"
    query = {"format": "json", "q": text_search}

    response = requests.get(api_url_for_search, params=query)
    json = response.json()
    first_result = json[0]
    lat_lon = {key: first_result[key] for key in first_result.keys()
               & {'lat', 'lon'}}
    lat_lon['lat'] = float(lat_lon['lat'])
    lat_lon['lon'] = float(lat_lon['lon'])
    return lat_lon

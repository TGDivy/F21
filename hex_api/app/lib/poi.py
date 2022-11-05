from geopoi import FetchPoi
from service.cache import cache
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class POI:
    def __init__(self, settings):
        value = settings['value']
        assert value

        # overwrite any defaults with user-supplied settings which will be the same as default if unchanged by user
        for user_setting_key in settings.keys():
            setattr(self, user_setting_key, settings[user_setting_key])


    def get_poi(self, place):
        results, pois_in_place_dataframe = get_poi(place, self.tag, values=[self.value])
        # pois_in_place_dataframe['color_for_poi'] = self.value
        # place_pubs_df.dropna(subset=['lat', 'lon'], inplace=True)
        return results, pois_in_place_dataframe


# memoization takes into account self argument of class methods resulting in different cache for each instantiation
# hence get_poi is defined outside
@cache.memoize(timeout=0)
def get_poi(place, tag, values):
    if 'API_ENDPOINT' in os.environ:
        fetch = FetchPoi(place, osm_endpoint=os.environ['API_ENDPOINT'])
    else:
        fetch = FetchPoi(place, osm_endpoint="https://osm.dev.npn.leapx.digital/api//interpreter")
    results, place_pubs_df = fetch.fetch_data(tag=tag, values=values)
    # place_pubs_df.dropna(subset=['lat', 'lon'], inplace=True)
    return results, place_pubs_df

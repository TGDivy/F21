import pandas as pd
from pyrosm import get_data
from pyrosm import OSM

if __name__ == "__main__":
    fp = get_data("London")
    osm = OSM(fp)

    custom_filter = {"amenity": True, "shop": True}
    landuse = osm.get_landuse()
    landuse.plot(column="landuse", legend=True, figsize=(10, 6))

    # print(pois.head())

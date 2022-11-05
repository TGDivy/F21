import pandas as pd
from pyrosm import get_data
from pyrosm import OSM
import matplotlib.pyplot as plt


class OpenStreetMap:
    def __init__(self, data_path):

        self.osm = OSM(get_data("london", directory=data_path))

    def get_data(self):
        landuse = self.get_landuse_data()
        # poi = self.get_point_of_interest_data()

        return (landuse,)

    def get_landuse_data(self):
        landuse = self.osm.get_landuse(
            custom_filter={"landuse": True, "lon": True, "lat": True}
        )

        # Drop all columns except for the longitude, latitude, and the type of landuse

        # Drow any row that has at least one NaN value
        # landuse.dropna(inplace=True)
        landuse.plot(column="landuse", legend=True, figsize=(10, 6))
        plt.show()

        # landuse = landuse[["lon", "lat", "landuse"]]

        return landuse

    def get_point_of_interest_data(self):
        poi = self.osm.get_pois(
            custom_filter={"amenity": True, "lon": True, "lat": True}
        )
        poi = poi[["lon", "lat", "amenity"]]
        poi.dropna(inplace=True)

        return poi


if __name__ == "__main__":
    osm = OpenStreetMap("data/osm")
    dfs = osm.get_data()

    for i, df in enumerate(dfs):
        df.to_csv(f"data/osm/{i}.csv", index=False)
    # print(df.head())
    # print(df.columns)
    # print(df["tags"].unique())

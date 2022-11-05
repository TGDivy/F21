import pandas as pd
from pyrosm import get_data
from pyrosm import OSM
import matplotlib.pyplot as plt


class OpenStreetMap:
    def __init__(self, data_path):

        self.osm = OSM(get_data("london", directory=data_path))

    def get_data(self):
        """_summary_

        Returns:
            _type_: List(List(Float, Float))
        """
        landuse = self.osm.get_landuse()
        landuse.plot(column="landuse", legend=True, figsize=(10, 6))
        plt.show()

        return landuse


if __name__ == "__main__":
    osm = OpenStreetMap("data/osm")
    df = osm.get_data()
    print(df.head())
    print(df.columns)
    print(df["tags"].unique())

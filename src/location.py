import sys

from data_extraction import DataExtraction
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from dataprep.clean import clean_lat_long

def main():
    database = pd.read_csv("../data/osm/London data - Data.csv")
    database = clean_lat_long(database, "Coordinates", split=True)


    # database['grid_id'] = grid_id
    database.to_csv('../data/preprocess/London data.csv')


if __name__ == "__main__":
    main()

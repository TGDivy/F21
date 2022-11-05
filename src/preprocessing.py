import sys

from data_extraction import DataExtraction
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm


def group_location():
    top_corner = [0.02, 51.58]
    bottom_corner = [-0.26, 51.39]
    x = np.arange(
        bottom_corner[0], top_corner[0], (top_corner[0] - bottom_corner[0]) / 20
    )
    y = np.arange(
        bottom_corner[1], top_corner[1], (top_corner[1] - bottom_corner[1]) / 20
    )
    x_grid, y_grid = np.meshgrid(x, y)
    rectangle_list = []
    for m in range(len(x_grid) - 1):
        for n in range(len(x_grid[m, :]) - 1):
            rectangle_list.append(
                [
                    [x_grid[m][n], y_grid[m, n]],
                    [x_grid[m + 1][n + 1], y_grid[m + 1, n + 1]],
                ]
            )
    return rectangle_list


def findrect(rect, point):
    if rect[0][0] < point[0] < rect[1][0] and rect[0][1] < point[1] < rect[1][1]:
        return True
    else:
        return False


class Preprocessing:
    def __init__(self) -> None:
        self.database = pd.read_csv(
            "data/uk_police_data/uk_police_data.csv", usecols=[5, 6, 10]
        )

        self.location_data = self.database.loc[:, ["Longitude", "Latitude"]].to_numpy()

        self.top_left, self.bottom_right = self.get_topLeft_bottomRight(
            self.location_data
        )
        self.Nheight = 200
        self.Nwidth = 200

        print(self.top_left, self.bottom_right)

        self.database["cell_id"] = self.database.apply(
            lambda x: self.get_cell_id((x["Longitude"], x["Latitude"])), axis=1
        )

        self.database.to_csv("data/uk_police_data/uk_police_data_cell.csv")

        self.database_osm = pd.read_csv("data/osm/POI.csv")

        self.location_data_osm = self.database_osm.loc[:, ["lon", "lat"]].to_numpy()

        self.database_osm["cell_id"] = self.database_osm.apply(
            lambda x: self.get_cell_id((x["lon"], x["lat"])), axis=1
        )

        self.database_osm.to_csv("data/osm/osm_data_cell.csv")

    def get_topLeft_bottomRight(self, points):
        x = [point[0] for point in points]
        y = [point[1] for point in points]
        return [min(x), max(y)], [max(x), min(y)]

    def get_cell_id(self, point):

        if point[0] < self.top_left[0] or point[0] > self.bottom_right[0]:
            return -1

        x = point[0]
        y = point[1]

        x_step = (self.bottom_right[0] - self.top_left[0]) / self.Nwidth
        y_step = (self.bottom_right[1] - self.top_left[1]) / self.Nheight

        x_id = int((x - self.top_left[0]) / x_step)
        y_id = int((y - self.top_left[1]) / y_step)

        return x_id + x_id * y_id


if __name__ == "__main__":
    Preprocessing()

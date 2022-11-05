import sys

from data_extraction import DataExtraction
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def group_location():
    top_corner = [0.02, 51.58]
    bottom_corner = [-0.26, 51.39]
    x = np.arange(bottom_corner[0], top_corner[0], (top_corner[0] - bottom_corner[0]) / 20)
    y = np.arange(bottom_corner[1], top_corner[1], (top_corner[1] - bottom_corner[1]) / 20)
    x_grid, y_grid = np.meshgrid(x, y)
    rectangle_list = []
    for m in range(len(x_grid) - 1):
        for n in range(len(x_grid[m, :]) - 1):
            rectangle_list.append([[x_grid[m][n], y_grid[m, n]], [x_grid[m + 1][n + 1], y_grid[m + 1, n + 1]]])
    return rectangle_list


def findrect(rect, point):
    if rect[0][0] < point[0] < rect[1][0] and rect[0][1] < point[1] < rect[1][1]:
        return True
    else:
        return False


def main():
    database = pd.read_csv("../data/uk_police_data/uk_police_data.csv", usecols=[5, 6, 10]).dropna()
    rectangle_list = group_location()
    location_data = database.loc[:, ["Longitude", "Latitude"]].to_numpy()
    grid_id = np.empty(len(database))
    for i, location in enumerate(location_data):
        out = [rectangle_list.index(rectangle) for rectangle in rectangle_list if np.any(findrect(rectangle, location))]
        if out:
            grid_id[i] = int(out[0])
    database['grid_id'] = grid_id
    database = database.dropna()
    database.to_csv('../data/preprocess/uk_police_data.csv')


if __name__ == "__main__":
    main()

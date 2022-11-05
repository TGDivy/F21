import sys

from data_extraction import DataExtraction
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def group_location():
    top_corner = [0.02, 51.58]
    bottom_corner = [-0.26, 51.39]
    x = np.arange(bottom_corner[0], top_corner[0], (top_corner[0] - bottom_corner[0]) / 3)
    y = np.arange(bottom_corner[1], top_corner[1], (top_corner[1] - bottom_corner[1]) / 3)
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
    database = pd.read_csv("../data/2022-09-city-of-london-outcomes.csv")
    database['rectangle'] = np.zeros(len(database), dtype=int)
    rectangle_list = group_location()
    location_data = database.loc[:, ["Longitude", "Latitude"]].to_numpy()
    for i, rectangle in enumerate(rectangle_list):
        database['rectangle'] = [i if findrect(rectangle, location) else None for location in location_data]
    database.to_csv('data_with_location.csv')


if __name__ == "__main__":
    main()

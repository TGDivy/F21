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
        self.Nheight = 400
        self.Nwidth = 400

        self.database["cell_id"] = self.database.apply(
            lambda x: self.get_cell_id((x["Longitude"], x["Latitude"])), axis=1
        )

        # self.database.to_csv("data/uk_police_data/uk_police_data_cell.csv")

        self.database_osm = pd.read_csv("data/osm/POI.csv")

        self.location_data_osm = self.database_osm.loc[:, ["lon", "lat"]].to_numpy()

        self.database_osm["cell_id"] = self.database_osm.apply(
            lambda x: self.get_cell_id((x["lon"], x["lat"])), axis=1
        )

        # self.database_osm.to_csv("data/osm/osm_data_cell.csv")

        # self.getCombinedData()

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

    def getCombinedData(self):
        uk_data = self.database
        grouped = uk_data.groupby("cell_id").count()
        grouped.drop(columns=["Longitude", "Latitude"], inplace=True)
        # grouped2 = self.database_osm.groupby("cell_id").

        # print(self.database_osm)
        self.database_osm.drop(columns=["lon", "lat"], inplace=True)

        # combine the two dataframes
        combined = grouped.merge(self.database_osm, how="outer", on="cell_id").fillna(0)
        # print(combined)
        combined = pd.get_dummies(combined, columns=["amenity"])

        combined = combined[combined.columns[combined.sum() > 5]]

        return combined


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error

if __name__ == "__main__":
    data = Preprocessing().getCombinedData()
    data = (data - data.mean()) / data.std()
    data.to_csv("data/uk_police_data_cell.csv")
    print(data)

    data["is_train"] = np.random.uniform(0, 1, len(data)) <= 0.80
    train, test = data[data["is_train"] == True], data[data["is_train"] == False]

    features = data.columns[3:]
    y = pd.factorize(train["Outcome type"])

    clf = RandomForestClassifier(
        n_jobs=2, random_state=0, max_depth=10, n_estimators=150
    )
    clf.fit(train[features], y[0])

    preds = clf.predict(test[features])
    preds = y[1][preds]
    pd.crosstab(
        test["Outcome type"], preds, rownames=["Actual"], colnames=["Predicted"]
    )

    # print test accuracy

    print("Accuracy: ", mean_squared_error(test["Outcome type"], preds))

    print((preds > 1).any())
    print((test["Outcome type"] > 1).any())

    # combine preds and test["Outcome type"] into a dataframe

    df = pd.DataFrame({"preds": preds, "test": test["Outcome type"]})
    df.to_csv("data/uk_police_data/preds.csv", index=False)

    # print feature importance

    print("Feature importance: ", clf.feature_importances_)

    # plot feature importance

    final_data = pd.DataFrame(
        {"feature": features[:10], "importance": clf.feature_importances_[:10]}
    )
    final_data.sort_values(by="importance", ascending=False, inplace=True)
    final_data.plot(kind="bar", x="feature", y="importance", figsize=(20, 10))

    plt.show()

    plt.barh(range(len(clf.feature_importances_)), clf.feature_importances_)

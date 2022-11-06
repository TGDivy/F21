import pandas as pd

CONSTANTS = {
    "TOP_LEFT": (51.699997, -0.5999968),
    "BOTTOM_RIGHT": (51.280014, 0.4199937),
}

# [
#     "Offender given a drugs possession warning",
#     "Offender given a caution",
#     "Local resolution",
# ]


def filter_by_month(df, month):
    return df[df["Month"] == month]


def filter_by_months(df, months):
    return df[df["Month"].isin(months)]


def filter_by_year(df, year):
    return df[df["Month"].str.contains(year)]


def within_bounds(lat: float, long: float):
    (top_left_lat, top_left_long), (bottom_right_lat, bottom_right_long) = (
        CONSTANTS["TOP_LEFT"],
        CONSTANTS["BOTTOM_RIGHT"],
    )
    return (
        top_left_lat >= lat >= bottom_right_lat
        and top_left_long <= long <= bottom_right_long
    )


def lat_long_to_id(lat: float, long: float, steps_x=40, steps_y=40):
    if not within_bounds(lat, long):
        return -1
    (top_left_lat, top_left_long), (bottom_right_lat, bottom_right_long) = (
        CONSTANTS["TOP_LEFT"],
        CONSTANTS["BOTTOM_RIGHT"],
    )

    width = top_left_long - bottom_right_long
    height = top_left_lat - bottom_right_lat

    x_step = width / steps_x
    y_step = height / steps_y

    x = int((long - bottom_right_long) / x_step)
    y = int((lat - bottom_right_lat) / y_step)

    return x + y * steps_x


def id_to_lat_long(id: int, steps_x=40, steps_y=40):
    (top_left_lat, top_left_long), (bottom_right_lat, bottom_right_long) = (
        CONSTANTS["TOP_LEFT"],
        CONSTANTS["BOTTOM_RIGHT"],
    )

    width = top_left_long - bottom_right_long
    height = top_left_lat - bottom_right_lat

    x_step = width / steps_x
    y_step = height / steps_y

    x = id % steps_x
    y = id // steps_x

    return (top_left_lat - y * y_step, bottom_right_long + x * x_step)


def get_data(weak_outcomes, month1, month2):
    poi = pd.read_csv("clean_data/poi.csv")
    uk_police_data = pd.read_csv("clean_data/uk_police_data.csv")

    uk_police_data = uk_police_data[~uk_police_data["Outcome type"].isin(weak_outcomes)]

    # Map latitude and longitude to the grid id
    poi["id"] = poi.apply(lambda row: lat_long_to_id(row["lat"], row["lon"]), axis=1)
    uk_police_data["id"] = uk_police_data.apply(
        lambda row: lat_long_to_id(row["Latitude"], row["Longitude"]), axis=1
    )

    # remove rows with -1 id
    poi = poi[poi["id"] != -1]
    uk_police_data = uk_police_data[uk_police_data["id"] != -1]

    # remove lat and lon columns, we don't need them anymore
    poi = poi.drop(columns=["lat", "lon"])
    uk_police_data = uk_police_data.drop(columns=["Latitude", "Longitude"])

    # Crimes in 2020 grouped by id
    crimes_date1 = (
        filter_by_month(uk_police_data, month1)
        .drop(columns=["Month"])
        .groupby("id")
        .count()
        .reset_index()
    )
    crimes_date1 = crimes_date1.rename(columns={"Outcome type": "Crime Count"})

    # Crimes in 2021 grouped by id
    crimes_date2 = (
        filter_by_month(uk_police_data, month2)
        .drop(columns=["Month"])
        .groupby("id")
        .count()
        .reset_index()
    )
    crimes_date2 = crimes_date2.rename(columns={"Outcome type": "Crime Count"})

    # Create 1 hot encoded columns for each amenity
    poi_main = poi.join(poi["amenity"].str.get_dummies(sep=";"))
    poi_main = poi_main.drop(columns=["amenity"])

    # Group by id and sum the 1 hot encoded columns
    poi_main = poi_main.groupby("id").sum().reset_index()

    # drop bench, post_box, waste_basket, bicycle_parking
    poi_main = poi_main.drop(
        columns=["bench", "post_box", "waste_basket", "bicycle_parking", "telephone"]
    )
    poi_main.drop(columns=["id"]).sum().sort_values(ascending=False)

    # merge crimes_2020 and poi_main
    merged_date1 = crimes_date1.merge(poi_main, on="id", how="left")
    merged_date1 = merged_date1.fillna(0)

    # merge crimes_2021 and poi_main
    merged_date2 = crimes_date2.merge(poi_main, on="id", how="left")
    merged_date2 = merged_date2.fillna(0)

    return merged_date1, merged_date2


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# plot feature importance
import matplotlib.pyplot as plt
import seaborn as sns

# create random forest model
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator


class Model:
    def __init__(self, weak_outcomes, model: BaseEstimator):
        self.weak_outcomes = weak_outcomes
        self.model = model

        self.normalise = False

    def train(self, merged_data):
        merged_data = merged_data.copy()
        # normalise data
        if self.normalise:
            merged_data = (merged_data - merged_data.mean()) / merged_data.std() + 1

        X_train, X_test, y_train, y_test = train_test_split(
            merged_data.drop(columns=["id", "Crime Count"]),
            merged_data["Crime Count"],
            test_size=0.2,
            random_state=42,
        )

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
        print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

    def predict(self, merged_data):
        merged_data = merged_data.copy()

        if self.normalise:
            merged_data = (merged_data - merged_data.mean()) / merged_data.std() + 1
        y_pred = self.model.predict(merged_data.drop(columns=["id", "Crime Count"]))

        return y_pred

    def predict_for_id(self, merged_data):
        y_pred = self.model.predict(
            merged_data[merged_data["id"] == id].drop(columns=["id", "Crime Count"])
        )

        return y_pred

    def get_id(self, lat, long):
        return lat_long_to_id(lat, long)


if __name__ == "__main__":
    year = 2020
    for month in range(1, 12):
        month1 = f"{year}-{month:02d}"
        month2 = f"{year}-{month + 1:02d}"
        model = Model(
            [
                # "Investigation complete; no suspect identified",
                # "Unable to prosecute suspect",
            ],
            RandomForestRegressor(n_estimators=100, random_state=42),
        )
        merged_date1, merged_date2 = get_data(model.weak_outcomes, month1, month2)

        print(f"Training model for {month1} and predicting for {month2}")

        if merged_date1.empty or merged_date2.empty:
            print("No data for this month")
            continue
        model.train(merged_date1)

        y_test = merged_date2["Crime Count"]
        y_pred = model.predict(merged_date2)

        print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
        print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))
        print("---------------------")

    # merged_date2["Crime Count Predicted"] = y_pred

    # merged_date2 = merged_date2.sort_values(by="Crime Count Predicted", ascending=False)

    # merged_date2 = merged_date2[["id", "Crime Count Predicted", "Crime Count"]]

    # merged_date2.to_csv("predicted_crime_count.csv", index=False)

    """
    The model is trained on the data from 2020 and then used to predict the crime count for 2021. The model is trained on the data from 2020 and then used to predict the crime count for 2021.
    """

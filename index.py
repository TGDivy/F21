from flask import Flask, jsonify, request
from src.uk_police_data import UKPoliceGetData
from test_script import Model, get_data
from sklearn.metrics import mean_squared_error, r2_score

# create random forest model
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

policeData = UKPoliceGetData("data/uk_police_data")


@app.route("/data", methods=["GET"])
def data():
    """_summary_

    Returns:
        _type_: List(List(Float, Float))
    """

    df = policeData.get_data()

    # filter by date
    if "date" in request.args:
        df = df[df["Month"] == request.args["date"]]
    else:
        df = df[df["Month"] == "2022-09"]
    # filter by crime type

    return jsonify(df.to_dict(orient="records"))


@app.route("/data", methods=["GET"])
def predict():
    year = 2020
    month = 1
    if "year" in request.args:
        year = int(request.args["year"])

    if "month" in request.args:
        month = int(request.args["month"])

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

    if merged_date1.empty or merged_date2.empty:
        print("No data for this month")
        return jsonify([])
    model.train(merged_date1)

    y_test = merged_date2["Crime Count"]
    y_pred = model.predict(merged_date2)

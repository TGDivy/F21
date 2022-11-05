from flask import Flask, jsonify, request
from uk_police_data import UKPoliceGetData

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

from flask import Flask, jsonify, request
from src.data_extraction import DataExtraction

app = Flask(__name__)

DE = DataExtraction(
    "./data/2022-09-city-of-london-outcomes.csv", ["Longitude", "Latitude"]
)


@app.route("/data", methods=["GET"])
def data():
    """_summary_

    Returns:
        _type_: List(List(Float, Float))
    """
    return {"data": DE.run()}

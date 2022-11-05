from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/data", methods=["GET"])
def hello_world():
    return {"data": "Hello World"}

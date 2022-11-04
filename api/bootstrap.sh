#!/bin/sh
export FLASK_APP=./src/index.py
flask --debug run -h 0.0.0.0
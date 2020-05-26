from exceptions.exceptions import *
from run import app
from flask import jsonify


@app.errorhandler(ChotuveError)
def handle(error):
    res = jsonify(error.to_dict())
    res.status_code = error.status_code
    return res
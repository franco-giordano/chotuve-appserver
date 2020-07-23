from exceptions.exceptions import *

from flask import jsonify


def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404


def handle(error):
    res = jsonify(error.to_dict())
    return res, error.status_code


def register_error_handlers(app):
    app.register_error_handler(404, not_found)
    app.register_error_handler(ChotuveError, handle)
from exceptions.exceptions import *

from flask import jsonify


def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404


def handle(error):
    res = jsonify(error.to_dict())
    res.status_code = error.status_code
    return res


def register_error_handlers(app):
    app.register_error_handler(404, not_found)
    app.register_error_handler(ChotuveError, handle)
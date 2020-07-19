from exceptions.exceptions import *

from flask import jsonify
from flask import jsonify, make_response

def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

def handle(error):
    response = make_response(jsonify(error.to_dict()), error.status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def register_error_handlers(app):
    app.register_error_handler(404, not_found)
    app.register_error_handler(ChotuveError, handle)
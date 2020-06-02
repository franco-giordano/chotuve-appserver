from functools import wraps
from flask import make_response, request
from services.authsender import AuthSender


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response({'message': 'Missing user token!'}, 401)

        if not AuthSender.is_valid_token(token):
            return make_response({'message': 'Token is invalid!'}, 401)

        return f(*args, **kwargs)

    return decorated

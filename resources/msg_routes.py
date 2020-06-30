
from flask_restful import Resource, reqparse

from daos.chats_dao import ChatsDAO

from services.authsender import AuthSender

from exceptions.exceptions import EndpointNotImplementedError, BadRequestError, UnauthorizedError

import logging


# /messages
class MessagesRoute(Resource):
    
    def __init__(self):
        super(MessagesRoute, self).__init__()
        
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        parser.add_argument("chat_with", location='json', type=int, required=True, help='You must specify which user are you chatting with')
        parser.add_argument("page", location='json', type=int, required=True, help='Page number to retrieve messages')
        parser.add_argument("per_page", location='json', type=int, required=True, help='Amount of messages to download')
        
        args = parser.parse_args()

        uuid1 = AuthSender.get_uuid_from_token(args['x-access-token'])

        msgs = ChatsDAO.get_messages_between(uuid1, args["chat_with"])

        return msgs, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        parser.add_argument("chat_with", location='json', type=int, required=True, help='You must specify which user are you chatting with')
        parser.add_argument("text", location='json', type=str, required=True, help='You must include the text to be sent!')
        
        args = parser.parse_args()

        sender_uuid = AuthSender.get_uuid_from_token(args['x-access-token'])

        msg = ChatsDAO.send_message(sender_uuid, args["chat_with"], args["text"])

        return msg, 200

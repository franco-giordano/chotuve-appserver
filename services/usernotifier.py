from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

from daos.users_dao import UsersDAO

import logging
from enum import Enum

class MessageTypes(Enum):
    MESSAGE = "message"
    FRIEND_REQ = "friend_req"


class UserNotifier():

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def send_notification(cls, user_id, title, subtitle, message_type, extra_data):
        
        token = UsersDAO.get_tkn(user_id)

        if not token:
            cls.logger().error(f"No token detected for user {user_id}. Unable to send push notification")
            return

        data = extra_data.copy()
        data["type"] = message_type

        cls._make_push(user_id, token, title, subtitle, data)


    @classmethod
    def _make_push(cls, user_id, token, title, subtitle, extra):
        try:
            response = PushClient().publish(
                PushMessage(to=token,
                            title=title,
                            body=subtitle,
                            data=extra))
        except PushServerError as exc:
            # Encountered some likely formatting/validation error.
            cls.logger().error(f"Failed to push notification. Token: {token}, Msg: {subtitle}, Extra: {extra}, Error: {exc.errors}, Response Data: {exc.response_data}")
            
        except (ConnectionError, HTTPError) as exc:
            # Encountered some Connection or HTTP error - retry a few times in
            # case it is transient.
            cls.logger().error(f"Failed to push notification. Token: {token}, Msg: {subtitle}, Extra: {extra}, Error: {exc}")


        try:
            # We got a response back, but we don't know whether it's an error yet.
            # This call raises errors so we can handle them with normal exception
            # flows.
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            UsersDAO.delete_tkn(user_id)
        except PushResponseError as exc:
            # Encountered some other per-notification error.
            cls.logger().error(f"Failed to push notification. Token: {token}, Msg: {subtitle}, Extra: {extra}, Error: {exc.errors}, Response Data: {exc.push_response._asdict}")

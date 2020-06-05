import requests
import os
import logging

from exceptions.exceptions import FailedToContactAuthSvError, NotFoundError, UnauthorizedError


class AuthSender():

    url = os.environ['CH_AUTHSV_URL'] if os.environ['APP_SETTINGS'] != 'testing' else None

    mock_db = []

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def is_valid_token(cls, token):
        if not cls.url:
            return True

        try:
            r = requests.post(cls.url + '/sign-in',
                              headers={'x-access-token': token})

            if r.status_code == 200:
                return True

            if r.status_code == 400:
                return False

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/sign-in with token {token}.")
            raise FailedToContactAuthSvError(
                f"Failed to contact sign-in backend.")

    @classmethod
    def get_uuid_from_token(cls, token):
        if not cls.url:
            cls._mock_get_info(int(token))
            return int(token)

        try:
            r = requests.get(cls.url + '/users/id',
                             headers={'x-access-token': token})
            if r.status_code != 200:
                raise NotFoundError(f"User with token {token} not found")

            return r.json()["uid"]

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users/id with token {token}.")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def get_user_info(cls, user_id, token):
        if not cls.url:
            return cls._mock_get_info(user_id)

        try:
            r = requests.get(cls.url + '/users/' + str(user_id),
                             headers={'x-access-token': token})
            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users/{user_id} with token {token}.")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def get_author_name(cls, user_id, token):
        if not cls.url:
            info, code = cls._mock_get_info(user_id)
            return info["display_name"]

        try:
            r = requests.get(cls.url + '/users/' + str(user_id),
                             headers={'x-access-token': token})
            
            return r.json()["display_name"]

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users/{user_id} with token {token}.")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def register_user(cls, fullname, email, phone, avatar, token):
        if not cls.url:
            return cls._mock_register(fullname, email, phone, avatar)
        try:
            r = requests.post(cls.url + '/users',
                              json={'email': email, 'display_name': fullname,
                                    'phone_number': phone, 'image_location': avatar},
                              headers={'x-access-token': token})

            cls.logger().debug(r)
            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users with token {token}.")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def modify_user(cls, user_id, args_dict):
        if not cls.url:
            return cls._mock_modify(user_id, args_dict)

        try:
            r = requests.post(cls.url + '/users' + str(user_id),
                              json=args_dict,
                              headers={'x-access-token': args_dict['x-access-token']})

            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users/{user_id} with token {args_dict['x-access-token']}.")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def _mock_register(cls, fullname, email, phone, avatar):
        user_id = len(cls.mock_db) + 1

        cls.mock_db.append({
            'email': email,
            'display_name': fullname,
            'phone_number': phone,
            'image_location': avatar,
            'id': user_id
        })

        return cls.mock_db[-1], 201

    @classmethod
    def _mock_get_info(cls, user_id):
        if not 0 < user_id <= len(cls.mock_db):
            raise NotFoundError(f"User with ID {user_id} not found")

        return cls.mock_db[user_id - 1], 200

    @classmethod
    def _mock_modify(cls, user_id, args_dict):
        if not 0 < user_id <= len(cls.mock_db):
            raise NotFoundError(f"User with ID {user_id} not found")

        if user_id != cls.get_uuid_from_token(args_dict["x-access-token"]):
            raise UnauthorizedError(f"You cant edit others info!")

        del args_dict["x-access-token"]

        for k in args_dict.keys():
            cls.mock_db[user_id - 1][k] = args_dict[k]

        return cls.mock_db[user_id - 1], 200

    @classmethod
    def msg_from_authsv(cls, json):
        json["from"] = "Authentication backend"
        return json

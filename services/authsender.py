import os
import logging

from exceptions.exceptions import NotFoundError, UnauthorizedError

from utils.requester import Requester


class AuthSender():

    url = os.environ['CH_AUTHSV_URL'] if os.environ['APP_SETTINGS'] != 'testing' else None

    mock_db = []

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def tkn_hdr(cls, token):
        return {'x-access-token': token}

    @classmethod
    def is_valid_token(cls, token):
        if not cls.url:
            return True

        msg, code = Requester.auth_fetch('POST', cls.url + '/sign-in', cls.tkn_hdr(token), payload={})

        if code == 200:
            return True

        if code == 400:
            return False


    @classmethod
    def get_uuid_from_token(cls, token):
        if not cls.url:
            cls._mock_get_info(int(token))
            return int(token)
        
        msg, code = Requester.auth_fetch('GET', cls.url + '/users/id', cls.tkn_hdr(token), payload={})

        if code != 200:
            raise NotFoundError(f"User with token {token[:10]}... not found")

        return msg["uid"]

    @classmethod
    def get_user_info(cls, user_id, token):
        if not cls.url:
            return cls._mock_get_info(user_id)

        return Requester.auth_fetch('GET', cls.url + f'/users/{user_id}', cls.tkn_hdr(token), payload={})



    @classmethod
    def get_author_name(cls, user_id, token):
        if not cls.url:
            info, code = cls._mock_get_info(user_id)
            return info["display_name"]

        msg, code = Requester.auth_fetch('GET', cls.url + f'/users/{user_id}', cls.tkn_hdr(token), payload={})
        return msg["display_name"]



    @classmethod
    def register_user(cls, fullname, email, phone, avatar, token, password=""):
        if not cls.url:
            return cls._mock_register(fullname, email, phone, avatar)

        payload = {'email': email, 'display_name': fullname,
                                    'phone_number': phone, 'image_location': avatar, 'password': password}

        return Requester.auth_fetch('POST', cls.url + '/users', cls.tkn_hdr(token), payload)


    @classmethod
    def modify_user(cls, user_id, args_dict):
        if not cls.url:
            return cls._mock_modify(user_id, args_dict)

        msg, code = Requester.auth_fetch('PUT', cls.url + '/users/' + str(user_id), cls.tkn_hdr(args_dict["x-access-token"]), args_dict)
        return msg, code


    @classmethod
    def find_user(cls, token, name=None, email=None, phone=None, per_page=None, page=None):
        if not cls.url:
            return cls._mock_find(name, email, phone)

        query = "?"

        if name:
            query += f"name={name}"
        if email:
            query += f"&email={email}"
        if phone:
            query += f"&phone={phone}"
        if per_page:
            query += f"&per_page={per_page}"
        if page:
            query += f"&page={page}"

        msg, code = Requester.auth_fetch('GET', cls.url + '/users' + query, cls.tkn_hdr(token), payload={})
        return msg, code



    @classmethod
    def delete_user(cls, user_id, token):
        if not cls.url:
            cls.mock_db[user_id-1] = {"DELETED":True}
            return
        msg, code = Requester.auth_fetch('DELETE', cls.url + f'/users/{user_id}', cls.tkn_hdr(token), payload={})
        return msg, code



    @classmethod
    def send_reset_code(cls, email):
        msg, code = Requester.auth_fetch('POST', cls.url + '/reset-codes', {}, payload={"email":email})
        return msg, code



    @classmethod
    def send_new_password(cls, email, reset_code, password):
        payload = {"email":email, "code": reset_code, "password": password}

        msg, code = Requester.auth_fetch('POST', cls.url + '/change-password-with-reset-code', {}, payload=payload)
        return msg, code


    # TODO: CAMBIAR TOKEN POR UUID!
    @classmethod
    def is_admin(cls, token):
        if not cls.url:
            return {"admin":False}, 200

        msg, code = Requester.auth_fetch('GET', cls.url + '/users/admin', cls.tkn_hdr(token), payload={})
        return msg, code

    @classmethod
    def is_user_admin(cls, uuid):
        if not cls.url:
            return {"admin":False}, 200

        msg, code = Requester.auth_fetch('GET', cls.url + '/users/' + str(uuid) + '/admin', {}, payload={})
        return msg, code

    
    @classmethod
    def has_permission(cls, user_id, viewer_id):
        return user_id == viewer_id or cls.is_user_admin(viewer_id)[0].get("admin", False)
        

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
    def _mock_find(cls, name=None, email=None, phone=None):
        found = cls.mock_db.copy()

        if name:
            found = [u for u in found if name in u["display_name"]]

        if email:
            found = [u for u in found if email == u["email"]]

        if phone:
            found = [u for u in found if phone == u["phone_number"]]

        return { 'users': found }, 200

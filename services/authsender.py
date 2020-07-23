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
            cls.logger().info(f"is_valid_token: Launching POST request at /sign-in for AuthSv with user token: {token[:10]}...")
            r = requests.post(cls.url + '/sign-in',
                              headers={'x-access-token': token})

            if r.status_code == 200:
                return True

            if r.status_code == 400:
                return False

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/sign-in with token {token[:10]}...")
            raise FailedToContactAuthSvError(
                f"Failed to contact sign-in backend.")

    @classmethod
    def get_uuid_from_token(cls, token):
        if not cls.url:
            cls._mock_get_info(int(token))
            return int(token)

        try:
            cls.logger().info(f"get_uuid_from_token: Launching GET request at /users/id for AuthSv with token: {token[:10]}...")
            r = requests.get(cls.url + '/users/id',
                             headers={'x-access-token': token})
            if r.status_code != 200:
                raise NotFoundError(f"User with token {token[:10]}... not found")

            return r.json()["uid"]

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users/id with token {token[:10]}...")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def get_user_info(cls, user_id, token):
        if not cls.url:
            return cls._mock_get_info(user_id)

        try:
            cls.logger().info(f"get_user_info: Launching GET request at /users/{user_id} for AuthSv with token: {token[:10]}...")
            r = requests.get(cls.url + '/users/' + str(user_id),
                             headers={'x-access-token': token})
            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users/{user_id} with token {token[:10]}...")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def get_author_name(cls, user_id, token):
        if not cls.url:
            info, code = cls._mock_get_info(user_id)
            return info["display_name"]

        try:
            cls.logger().info(f"get_author_name: Launching GET request at /users/{user_id} for AuthSv with token: {token[:10]}...")
            r = requests.get(cls.url + '/users/' + str(user_id),
                             headers={'x-access-token': token})
            
            return r.json()["display_name"]

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users/{user_id} with token {token[:10]}...")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def register_user(cls, fullname, email, phone, avatar, token, password=""):
        if not cls.url:
            return cls._mock_register(fullname, email, phone, avatar)

        payload = {'email': email, 'display_name': fullname,
                                    'phone_number': phone, 'image_location': avatar, 'password': password}

        try:
            cls.logger().info(f"register_user: Launching POST request at /users for AuthSv with token: {token[:10]}... . Payload: {payload}")
            r = requests.post(cls.url + '/users',
                              json=payload,
                              headers={'x-access-token': token})

            cls.logger().debug(r)
            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users with token {token[:10]}...")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def modify_user(cls, user_id, args_dict):
        if not cls.url:
            return cls._mock_modify(user_id, args_dict)

        try:
            cls.logger().info(f"modify_user: Launching PUT request at /users/{user_id} for AuthSv with token: {args_dict['x-access-token'][:10]}... . Payload: {args_dict}")
            r = requests.put(cls.url + '/users/' + str(user_id),
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

        try:
            cls.logger().info(f"find_user: Launching GET request at /users for AuthSv with token: {token[:10]}... . Query args: {query}")
            r = requests.get(cls.url + '/users' + query,
                              headers={'x-access-token': token})

            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users?name={name}&phone={phone}&email={email}&per_page={per_page}&page={page} with token {token[:10]}.")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def delete_user(cls, user_id, token):
        if not cls.url:
            cls.mock_db[user_id-1] = {"DELETED":True}
            return

        try:
            cls.logger().info(f"delete_user: Launching DELETE request at /users/{user_id} for AuthSv")
            r = requests.delete(cls.url + f'/users/{user_id}')

            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users/{user_id}")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")


    @classmethod
    def send_reset_code(cls, email):
        try:
            cls.logger().info(f"send_reset_code: Launching POST request at /reset-codes for AuthSv with email: {email}")
            r = requests.post(cls.url + '/reset-codes',
                              json={"email":email})

            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/reset-codes with email {email}.")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    @classmethod
    def send_new_password(cls, email, reset_code, password):
        try:
            cls.logger().info(f"send_new_password: Launching POST request at /change-password-with-reset-codes for AuthSv with email: {email}, reset_code: {reset_code}, password: ********")
            r = requests.post(cls.url + '/change-password-with-reset-code',
                              json={"email":email, "code": reset_code, "password": password})

            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/change-password-with-reset-codes with email {email}, reset_code: {reset_code}.")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")

    # TODO: CAMBIAR TOKEN POR UUID!
    @classmethod
    def is_admin(cls, token):
        if not cls.url:
            return {"admin":False}, 200

        try:
            cls.logger().info(f"is_admin: Launching GET request at /users/admin for AuthSv with token: {token[:10]}")
            r = requests.get(cls.url + '/users/admin',
                              headers={"x-access-token":token})

            msg = cls.msg_from_authsv(r.json())
            return msg, r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact AuthSv at url {cls.url}/users/admin")
            raise FailedToContactAuthSvError(
                f"Failed to contact user backend.")
    
    @classmethod
    def has_permission(cls, user_id, viewer_id):
        # TODO FIX IS_ADMIN!
        return user_id == viewer_id # or cls.is_admin(viewer_id)
        

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

    @classmethod
    def msg_from_authsv(cls, json):
        json["from"] = "Authentication backend"
        return json

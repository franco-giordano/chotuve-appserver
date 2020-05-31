import requests
import os, logging

from exceptions.exceptions import FailedToContactAuthSvError, NotFoundError

# TODO hace cualquier cosa!
class AuthSender():

    url = os.environ['CH_AUTHSV_URL'] if os.environ['APP_SETTINGS'] != 'development' else None

    mock_db = []

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)



    @classmethod
    def is_valid_token(cls, token):
        if not cls.url:
            return True

        try:
            r = requests.post(cls.url + '/sign-in', headers={'x-access-token':token})

            if r.status_code == 200:
                return True

            if r.status_code == 401:
                return False

        except requests.exceptions.RequestException:
            cls.logger().error(f"Failed to contact AuthSv at url {cls.url}/sign-in with token {token}.")
            raise FailedToContactAuthSvError(f"Failed to contact sign-in backend.")

    @classmethod
    def get_uuid_from_token(cls, token):
        if not cls.url:
            return int(token)

        try:
            r = requests.get(cls.url + '/users/id', headers={'x-access-token':token})
            return r.json()["uid"]

        except requests.exceptions.RequestException:
            cls.logger().error(f"Failed to contact AuthSv at url {cls.url}/users/id with token {token}.")
            raise FailedToContactAuthSvError(f"Failed to contact user backend.")

    @classmethod
    def get_user_info(cls, user_id, token):
        if not cls.url:
            return cls._mock_get_info(user_id)

        try:
            r = requests.get(cls.url + '/users/' + user_id, headers={'x-access-token':token})
            return r.json(), r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(f"Failed to contact AuthSv at url {cls.url}/users/{user_id} with token {token}.")
            raise FailedToContactAuthSvError(f"Failed to contact user backend.")


    # TODO AUTHSV DEBE MANDARME USERID EN LA RTA
    @classmethod
    def register_user(cls, fullname, email, phone, avatar, token):
        if not cls.url:
            return cls._mock_register(fullname, email, phone, avatar)
        try:    
            r = requests.post(cls.url + '/sign-up', 
                json={'email':email, 'display_name':fullname, 'phone_number':phone, 'image_location': avatar},
                headers={'x-access-token': token})

            return r.json(), r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(f"Failed to contact AuthSv at url {cls.url}/sign-up with token {token}.")
            raise FailedToContactAuthSvError(f"Failed to contact user backend.")



    @classmethod
    def modify_user(cls, user_id, args_dict):
        if not cls.url:
            return cls._mock_modify(user_id,args_dict)

        try:
            r = requests.post(cls.url + '/users' + user_id, 
                json=args_dict,
                headers={'x-access-token': args_dict['x-access-token']})

            return r.json(), r.status_code
            
        except requests.exceptions.RequestException:
            cls.logger().error(f"Failed to contact AuthSv at url {cls.url}/users/{user_id} with token {args_dict['x-access-token']}.")
            raise FailedToContactAuthSvError(f"Failed to contact user backend.")


    @classmethod
    def _mock_register(cls, fullname, email, phone, avatar):
        user_id = len(cls.mock_db)+1

        cls.mock_db.append({
            'email':email,
            'display_name':fullname,
            'phone_number':phone,
            'image_location':avatar,
            'id':user_id
        })

        return cls.mock_db[-1], 201

    @classmethod
    def _mock_get_info(cls, user_id):
        if not 0 < user_id <= len(cls.mock_db):
            raise NotFoundError(f"User with ID {user_id} not found")
        
        return cls.mock_db[user_id-1], 200

    @classmethod
    def _mock_modify(cls, user_id, args_dict):
        if not 0 < user_id <= len(cls.mock_db):
            raise NotFoundError(f"User with ID {user_id} not found")
        
        del args_dict["x-access-token"]

        cls.mock_db[user_id-1] = args_dict

        return cls.mock_db[user_id-1], 200

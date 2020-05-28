import requests
import os, logging

from exceptions.exceptions import FailedToContactAuthSvError

# TODO hace cualquier cosa!
class AuthSender():

    url = os.environ['CH_AUTHSV_URL'] if os.environ['APP_SETTINGS'] != 'development' else None

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
        #

        return int(token)

    @classmethod
    def get_user_info(cls, user_id, token):
        if not cls.url:
            return {'id':user_id, 
                'email':'example@example.com',
                'display_name':'John Smith',
                'phone_number':'+5423643265',
                'image_location':"https://image.freepik.com/foto-gratis/playa-tropical_74190-188.jpg"}, 200



        try:
            r = requests.get(cls.url + '/users/' + user_id, headers={'x-access-token':token})
            return r.json(), r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(f"Failed to contact AuthSv at url {cls.url}/users/{user_id} with token {token}.")
            raise FailedToContactAuthSvError(f"Failed to contact user backend.")



    @classmethod
    def register_user(cls, fullname, email, phone, avatar, token):
        if not cls.url:
            return {'id':123, 
                'email':'example@example.com',
                'display_name':'John Smith',
                'phone_number':'+5423643265',
                'image_location':"https://image.freepik.com/foto-gratis/playa-tropical_74190-188.jpg"}, 200

        
        r = requests.post(cls.url + '/sign-up', 
            json={'email':email, 'display_name':fullname, 'phone_number':phone, 'image_location': avatar},
            headers={'x-access-token': token})

        return r.json(), r.status_code

    @classmethod
    def modify_user(cls, user_id, args_dict):
        if not cls.url:
            return args_dict, 200

        
        r = requests.post(cls.url + '/users' + user_id, 
            json=args_dict,
            headers={'x-access-token': args_dict['x-access-token']})

        return r.json(), r.status_code
        

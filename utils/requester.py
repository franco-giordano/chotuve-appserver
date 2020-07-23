from exceptions.exceptions import BadGatewayError
import requests
import os
import logging


class Requester():

    MEDIA_TOKEN = os.environ['CH_MEDIASV_TOKEN'] if os.environ['APP_SETTINGS'] != 'testing' else ''
    AUTH_TOKEN = os.environ['CH_AUTHSV_TOKEN'] if os.environ['APP_SETTINGS'] != 'testing' else ''

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)


    @classmethod
    def _fetch(method, url, headers, payload):
        try:
            cls.logger().info(f"Launching {method} request at {url}. Payload: {payload}")
            cls.logger().debug(f"Using extra headers: {extra_headers}")

            r = requests.request(method, url,
                              json=payload,
                              headers=headers)

            return r.json(), r.status_code

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact {url} with method {method} and payload {payload}")
            raise BadGatewayError(
                f"Failed to contact external resource.")

    @classmethod
    def media_fetch(cls, method, url, extra_headers, payload):
        header = {"x-client-token": MEDIA_TOKEN}
        header.update(extra_headers)

        return cls._fetch(method, url, header, payload)
    
    @classmethod
    def auth_fetch(cls, method, url, extra_headers, payload):
        header = {"x-client-token": AUTH_TOKEN}
        header.update(extra_headers)

        return cls._fetch(method, url, header, payload)
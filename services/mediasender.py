import requests
import os

import logging


import datetime


class MediaSender():

    url = os.environ['CH_MEDIASV_URL'] if os.environ['APP_SETTINGS'] != 'testing' else None

    mock_db = {}

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def send_url(cls, vid_id, fb_url):
        if not cls.url:
            return cls._mock_send(vid_id, fb_url)
        
        payload = {'videoId': vid_id, 'url': fb_url}

        try:
            cls.logger().info(f"send_url: Launching POST request at /video for MediaSv. Payload: {payload}")
            r = requests.post(cls.url + '/video',
                              json=payload)

            if r.status_code != 201:
                cls.logger().error(f"Error uploading video for ID: {vid_id}. Response: {r.json()}, code {r.status_code}")


            cls.logger().debug(f"MediaSv response: {r.json()}")
            return r.json()['url'], r.json()['timestamp']

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact MediaSv at url {cls.url}/video with payload videoId: {vid_id}, url:{fb_url}.")


    @classmethod
    def get_info(cls, vid_id):

        if not cls.url:
            return cls._mock_get(vid_id)

        try:
            cls.logger().info(f"send_url: Launching GET request at /video for MediaSv at video {vid_id}")
            r = requests.get(cls.url + '/video', json={'videoId': vid_id})

            if r.status_code != 200:
                cls.logger().error(f"Error getting video info for ID: {vid_id}. Response: {r.json()}, code {r.status_code}")


            return r.json()['url'], r.json()['timestamp']

        except requests.exceptions.RequestException:
            cls.logger().error(
                f"Failed to contact MediaSv at url {cls.url}/video with payload videoId: {vid_id}.")


    @classmethod
    def _mock_send(cls, vid_id, fb_url):
        cls.mock_db[vid_id] = (fb_url, str(datetime.datetime.now(datetime.timezone.utc)))

        return fb_url, cls.mock_db[vid_id][1]

    @classmethod
    def _mock_get(cls, vid_id):
        vid_url, timestamp = cls.mock_db.get(vid_id)

        return vid_url, timestamp

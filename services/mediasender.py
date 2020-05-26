import requests
import os

import logging

from exceptions.exceptions import FailedToContactMediaSvError


class MediaSender():

    url = os.environ['CH_MEDIASV_URL'] if os.environ['APP_SETTINGS'] == 'production' else None

    mock_db = {}

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)


    @classmethod
    def send_url(cls, vid_id,fb_url):
        if not cls.url:
            return cls._mock_send(vid_id, fb_url)

        try:
            r = requests.post(cls.url + '/video', json={'videoId': vid_id, 'url': fb_url})

            if r.status_code != 201:
                raise FailedToContactMediaSvError(f"Failed to upload video. Response {r.status_code}")

            return r.json()['url'], r.json()['timestamp']
            
        except requests.exceptions.RequestException:
            cls.logger().error(f"Failed to contact MediaSv at url {cls.url}/video with payload videoId: {vid_id}, url:{fb_url}.")
            raise FailedToContactMediaSvError(f"Failed to upload video to media backend.")


    @classmethod
    def get_info(cls,vid_id):

        if not cls.url:
            return cls._mock_get(vid_id)

        cls.logger().info(f"Sending request to {cls.url}")

        try:
            r = requests.get(cls.url + '/video', json={'videoId': vid_id})

            if r.status_code != 200:
                raise FailedToContactMediaSvError(f"Failed to get video info. Response {r.status_code}")

            return r.json()['url'], r.json()['timestamp']

        except requests.exceptions.RequestException:
            cls.logger().error(f"Failed to contact MediaSv at url {cls.url}/video with payload videoId: {vid_id}.")
            raise FailedToContactMediaSvError(f"Failed to get video info for {vid_id}.")

    @classmethod
    def _mock_send(cls, vid_id, fb_url):
        cls.mock_db[vid_id] = fb_url

        return fb_url, "PREV_TIMESTAMP"

    @classmethod
    def _mock_get(cls, vid_id):
        vid_url = cls.mock_db.get(vid_id, "PREVIOUS_URL")

        return vid_url, "PREV_TIMESTAMP"

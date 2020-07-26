from flask_restful import Resource
from daos.http_daos import httpDAO

from daos.videos_dao import VideoDAO
from daos.users_dao import UsersDAO

# /stats
class StatsRoutes(Resource):

    def get(self):

        count = httpDAO.count_total()

        requests_per_hour = httpDAO.count_reqs_per_hour()

        requests_per_method = httpDAO.count_reqs_per_method()

        requests_per_response = httpDAO.count_reqs_per_response_code()

        registered_users = httpDAO.count_registered_users_in_30_days()

        new_vids = httpDAO.count_uploaded_vids_in_30_days()

        new_cmnts = httpDAO.count_posted_comments_in_30_days()

        #--- non-http stats:

        private_vids_count, total_vids_count = VideoDAO.count_private_over_total_vids()

        total_registered_users_count = UsersDAO.count_total_registered_users()

        return {
            "requests_per_hour": requests_per_hour,
            "requests_per_method": requests_per_method,
            "requests_per_code": requests_per_response,
            "new_users_in_last_30_days": registered_users,
            "new_vids_in_last_30_days": new_vids,
            "new_cmnts_in_last_30_days": new_cmnts,
            "private_and_total_vids_count": [private_vids_count, total_vids_count],
            "registered_users_count": total_registered_users_count,
            "total_count": count
        }
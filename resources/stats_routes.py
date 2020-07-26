from flask_restful import Resource
from daos.http_daos import httpDAO


# /stats
class StatsRoutes(Resource):

    def get(self):

        count = httpDAO.count_total()

        requests_per_hour = httpDAO.count_reqs_per_hour()

        requests_per_method = httpDAO.count_reqs_per_method()

        requests_per_response = httpDAO.count_reqs_per_response_code()

        registered_users = httpDAO.count_registered_users_in_30_days()

        new_vids = httpDAO.count_uploaded_vids_in_30_days()

        return {
            "requests_per_hour": requests_per_hour,
            "requests_per_method": requests_per_method,
            "requests_per_code": requests_per_response,
            "new_users_in_last_30_days": registered_users,
            "new_vids_in_last_30_days": new_vids,
            "total_count": count
        }
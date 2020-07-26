from flask_restful import Resource
from daos.http_daos import httpDAO


# /stats
class StatsRoutes(Resource):

    def get(self):

        count = httpDAO.count_total()

        requests_per_hour = httpDAO.count_reqs_per_hour()

        requests_per_method = httpDAO.count_reqs_per_method()

        requests_per_response = httpDAO.count_reqs_per_response_code()

        return {
            "requests_per_hour": requests_per_hour,
            "requests_per_method": requests_per_method,
            "requests_per_code": requests_per_response,
            "total_count": count
        }
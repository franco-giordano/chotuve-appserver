from run import app
import unittest

class FlaskTest(unittest.TestCase):


    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")

        statuscode = response.status_code
        self.assertEqual(statuscode, 404)


    def test_videos_type(self):
        tester = app.test_client(self)
        response = tester.get("/video")

        self.assertEqual(response.content_type, "application/json")


if __name__ == "__main__":
    unittest.main()
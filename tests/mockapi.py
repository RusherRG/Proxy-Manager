import unittest
import requests

MOCKAPI = "http://localhost:5555"


class TestMockapi(unittest.TestCase):
    """
    Test cases for flask mockapi server
    """

    def test_api(self):
        headers = {"key": "XYZ"}
        response = requests.get(MOCKAPI + "/api", headers=headers)
        message = response.json().get("message", "")
        self.assertIsNotNone(message)

    def test_api_limit(self):
        headers = {"key": "ABC"}
        for i in range(10):
            response = requests.get(MOCKAPI + "/api", headers=headers)

        response = requests.get(MOCKAPI + "/api", headers=headers)
        message = response.json().get("message", "")
        self.assertTrue("Limit Reached" in message)

    def test_proxy(self):
        data = {"dummy": "data"}
        response = requests.post(MOCKAPI + "/proxy",
                                 data=data)
        message = response.json().get("message", "")
        self.assertIsNotNone(message)

    def test_proxy_limit(self):
        data = {"dummy": "data"}
        for i in range(10):
            response = requests.post(MOCKAPI + "/proxy",
                                     data=data)
        response = requests.post(MOCKAPI + "/proxy",
                                 data=data)
        message = response.json().get("message", "")
        self.assertTrue("Limit Reached" in message)

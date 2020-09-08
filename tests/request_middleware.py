import unittest
from request_middleware.request import Request

URL = "http://localhost:5555/{}"


class RequestMiddlewareTest(unittest.TestCase):
    def test_request_api(self):
        req = Request("key", "test_api", cache=False)
        key = req.get_key_proxy()
        headers = {"key": key}
        for i in range(5):
            response = req.send("GET", URL.format("api"),
                                headers=headers, data={"dummy": "data"}).json()
            self.assertTrue(key in response.get("message", ""))
        req.close_session()

        req = Request("key", "test_api", cache=False)
        key2 = req.get_key_proxy()
        self.assertNotEquals(key, key2)

        headers = {"key": key2}
        for i in range(5):
            response = req.send("GET", URL.format("api"),
                                headers=headers, data={"dummy": "data"}).json()
            self.assertTrue(key2 in response.get("message", ""))
        req.close_session()

    def test_request_proxy(self):
        req = Request("ip", "test_proxy", cache=False)
        ip = req.get_key_proxy()
        req.add_user_agent()
        proxies = {
            "http": "http://" + ip,
            "https": "https://" + ip
        }
        response = req.send("POST", URL.format("proxy"),
                            proxies=proxies, data={"dummy": "data"})
        response = response.json()
        self.assertTrue(ip in response.get("message", ""))
        ip2 = req.get_key_proxy()
        req.add_user_agent()
        self.assertNotEquals(ip, ip2)
        proxies = {
            "http": "http://" + ip,
            "https": "https://" + ip
        }
        response = req.send("POST", URL.format("proxy"),
                            proxies=proxies, data={"dummy": "data"}).json()
        self.assertTrue(ip in response.get("message", ""))
        req.close_session()

    def test_cache(self):
        req = Request("key", "test_api", cache=True)
        key = req.get_key_proxy()
        headers = {"key": key}
        response = req.send("GET", URL.format("api"),
                            headers=headers, data={"dummy": "data"}).json()
        new_response = req.send("GET", URL.format("api"),
                                headers=headers,
                                data={"dummy": "new_data"}).json()
        self.assertEquals(response.get("data"), new_response.get('data'))
        req.close_session()

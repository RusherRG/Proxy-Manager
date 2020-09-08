from request_middleware.request import Request

URL = "http://localhost:5555/{}"


def request_api():
    req = Request("key", "test_api", cache=False)
    key = req.get_key_proxy()
    headers = {"key": key}
    for i in range(5):
        response = req.send("GET", URL.format("api"),
                            headers=headers, data={"dummy": "data"}).json()
    req.close_session()

    req = Request("key", "test_api", cache=False)
    key2 = req.get_key_proxy()

    headers = {"key": key2}
    for i in range(5):
        response = req.send("GET", URL.format("api"),
                            headers=headers, data={"dummy": "data"}).json()
    req.close_session()


def request_proxy():
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

    ip2 = req.get_key_proxy()
    req.add_user_agent()
    proxies = {
        "http": "http://" + ip,
        "https": "https://" + ip
    }
    response = req.send("POST", URL.format("proxy"),
                        proxies=proxies, data={"dummy": "data"}).json()
    req.close_session()


if __name__ == "__main__":
    request_api()
    request_proxy()

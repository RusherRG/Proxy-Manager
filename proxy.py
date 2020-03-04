import random
import requests
import threading
import string

letters = string.ascii_letters + string.digits


def send_request():
    url = "https://webhook.site/360d7cf8-4df7-4069-b5cf-6dc789bb6de0"
    method = ['GET', 'POST'][random.randint(0, 1)]
    if method == 'GET':
        params = {
            'url': url,
            'param1': ''.join([letters[random.randint(0, len(letters)-1)]
                               for i in range(5)]),
            'param2': ''.join([letters[random.randint(0, len(letters)-1)]
                               for i in range(5)])
        }
        response = requests.get('http://127.0.0.1:5000', params=params)
    else:
        data = {
            'url': url,
            'name': ''.join([letters[random.randint(0, len(letters)-1)]
                             for i in range(5)]),
            'title': ''.join([letters[random.randint(0, len(letters)-1)]
                              for i in range(5)])
        }
        response = requests.post('http://127.0.0.1:5000', data=data)

    print(response.text)


if __name__ == "__main__":
    for _ in range(1):
        threads = []
        for i in range(20):
            thread = threading.Thread(target=send_request)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

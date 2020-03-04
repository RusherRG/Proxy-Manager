from flask import Flask, request
import requests
import logging
import colorlog
import logstash

from datetime import datetime
from elasticsearch import Elasticsearch

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value,
                     OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems,
    limit=100)

app = Flask(__name__)
app.config.from_object('config')

es = Elasticsearch(hosts="http://elastic:1234567Ee@localhost:9200/")


@app.route('/', methods=['GET', 'POST'])
def proxy():
    print("request")
    ip = request.remote_addr
    headers = dict(request.headers)
    data, params, response, url = None, None, None, None
    logger = get_logger()
    logger.debug("Received request from ip: {}".format(ip).encode())

    if 'Host' in headers:
        del headers['Host']
    headers['User-Agent'] = user_agent_rotator.get_random_user_agent()
    try:
        if request.method == 'GET':
            params = dict(request.args)
            url = params.get('url').strip()
            logger.info("Sending GET request to url: {}".format(url))
            response = requests.get(url, headers=headers, params=params)
        elif request.method == 'POST':
            data = request.form
            if data.get('url') is None:
                data = request.get_json(force=True)
            url = data.get('url').strip()
            logger.info("Sending POST request to url: {}".format(url))
            response = requests.post(url, headers=headers, data=data)
    except Exception as err:
        print(err)
        logger.error(err)

    try:
        logger.info("Response received")
        body = {
            "ip": ip,
            "request": {
                "url": url,
                "method": request.method,
                "headers": headers,
                "data": params if request.method == 'GET' else data
            },
            "response": response.text,
            "timestamp": str(datetime.now()),
        }
        logger.info("Logging information to ElasticSearch")
        es.index(index="requests", body=body)
        logger.info("Request completed")
    except Exception as err:
        logger.error(err)
    if response is not None:
        return {
            'response': response.text,
            'status': response.status_code
        }
    else:
        return {
            'response': "Some error occurred",
            'status': 500
        }


def get_logger():
    # bold_seq = '\033[1m'
    # colorlog_format = (
    #     f'{bold_seq} '
    #     '%(log_color)s '
    #     f'%(asctime)s | %(name)s/%(funcName)s | %(levelname)s: %(message)s'
    # )
    # colorlog.basicConfig(format=colorlog_format.encode(),
    #                      level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S %p'.encode())
    logger = logging.getLogger("Server")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logstash.TCPLogstashHandler(
        'localhost', 6000, version=1))

    return logger


if __name__ == '__main__':
    app.run(host="0.0.0.0")

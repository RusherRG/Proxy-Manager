from datetime import datetime
from elasticsearch import Elasticsearch
from utils import get_logger

logger = get_logger(__name__)
es = Elasticsearch(hosts="http://elastic:1234567Ee@localhost:9200/")


def fetch_secrets():
    """
    Fetch the secrets json from Elasticsearch
    """
    logger.info("Fetching secrets")
    secrets_json = es.get(index="secrets", id=1)
    if not secrets_json.get("found", False):
        logger.error("Secrets config not found")
    secrets_json = secrets_json.get("_source", {})
    return secrets_json


def post_secrets(secrets_json):
    """
    Posts the new secrets json from Elasticsearch
    """
    logger.info("Posting secrets to ElasticSearch")
    es.index(index="secrets", body=secrets_json, id=1)
    return


def get_cached_response(request_query):
    """
    Given the request_query, cache index in Elasticsearch is searched to find
    a match and the cached response is returned
    """
    logger.info("Checking cache")
    for d in ["data", "params"]:
        if d in request_query:
            for key, value in request_query[d].items():
                request_query[d+"."+key] = value
            del request_query[d]
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {key: value}}
                    for key, value in request_query.items()
                    if len(value)
                ]
            }
        }
    }
    response = None
    try:
        result = es.search(index="cache", body=body, size=1)
        hits = result["hits"]["hits"]
        if len(hits):
            response = hits[0]["_source"]["response"]
    except Exception as err:
        logger.error(err)

    return response


def cache_response(method, url, data, params, response):
    """
    Caches the response in cache index
    """
    logger.info("Caching response")
    response_json = response.__dict__
    res = {}
    for key in ["content", "text", "json", "html"]:
        if key in response_json:
            res[key] = response_json[key]
    body = {
        "method": method,
        "url": url,
        "data": data,
        "params": params,
        "response": res
    }
    try:
        es.index(index="cache", body=body)
    except Exception as err:
        logger.error(err)

    return


def log_request(**kwargs):
    """
    Logs the request so that it could be used by Kibana to plot dashboard
    """
    logger.info("Logging request")
    body = kwargs
    body["timestamp"] = str(datetime.now())
    try:
        es.index(index="request_logs", body=body)
    except Exception as err:
        logger.error(err)

    return

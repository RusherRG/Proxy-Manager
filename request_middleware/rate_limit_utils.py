import os
import sys
import json
import math
import time

from utils import get_logger
from .elasticsearch_utils import fetch_secrets, post_secrets

logger = get_logger(__name__)


def update_secrets(file_path="configs/secrets.json"):
    """
    Updates the secrets document in Elasticsearch using the given file_path
    """
    if not os.path.isfile(file_path):
        logger.error("File not found: '{}'".format(file_path))
        return

    with open(file_path, "r") as f:
        secrets_json = json.load(f)
        logger.info("Restructing 'secrets.json'")
        secrets = {
            "key_based": {},
            "ip_based": {},
            "last_update": int(time.time())
        }
        for secret_type in ["key_based", "ip_based"]:
            for endpoint, keys in secrets_json.get(secret_type, {}).items():
                secrets[secret_type][endpoint] = {
                    "limit": keys.get("limit", sys.maxsize),
                    "refresh_rate": keys.get("refresh_rate", sys.maxsize)
                }
                if "key" in secret_type:
                    secrets[secret_type][endpoint]["keys"] = {}
                    for key in keys.get("keys", []):
                        secrets[secret_type][endpoint]["keys"][key] = 0
                else:
                    secrets[secret_type][endpoint]["ips"] = {}
                    for ip in secrets_json.get("ips", []):
                        secrets[secret_type][endpoint]["ips"][ip] = 0

        post_secrets(secrets)

    return


def get_secret(secret_type, endpoint):
    """
    Fetches the secret with the least usage count from elasticsearch
    """
    secrets_json = fetch_secrets()
    secrets = secrets_json.get(
        secret_type+"_based", {}).get(endpoint, {}).get(secret_type+"s", {})
    limit = secrets_json.get(secret_type+"_based", {}
                             ).get(endpoint, {}).get("limit")
    if not secrets:
        logger.error("No {}s found for {}".format(secret_type, endpoint))
        return None
    logger.info("Fetch {} for {}".format(secret_type, endpoint))
    min_usage = math.inf
    secret = None
    print(secrets)
    for sec, usage in secrets.items():
        if usage < min_usage and usage < limit:
            secret = sec
            min_usage = usage
    if secret is None:
        logger.warn("No secrets under limit")
    return secret


def get_key(endpoint):
    key = get_secret("key", endpoint)
    return key


def get_proxy(endpoint):
    ip = get_secret("ip", endpoint)
    return ip


def update_count(secret_type, endpoint, secret, count):
    """
    Updates the usage count of a particular secret
    """
    logger.info("Updating count {} by {}".format(endpoint, count))
    secrets_json = fetch_secrets()
    secrets_json[secret_type+"_based"][endpoint][secret_type+"s"][secret] += \
        count
    post_secrets(secrets_json)
    return


def reset_limits():
    """
    Fetch the secrets json. For each secret present in the json if the time
    elapsed since last_update is greater than it's refresh time, the count is
    updated
    """
    secrets_json = fetch_secrets
    last_update = secrets_json.get("last_update", time.time())
    time_difference = (time.time() - last_update) // 60
    for secret_type in secrets_json:
        for endpoint, keys in secrets_json.get(secret_type, {}).items():
            if time_difference < endpoint["refresh_rate"]:
                continue
            logger.info("Resetting limits for {}".format(endpoint))
            dict_key = "keys" if "key" in secret_type else "ips"
            for key in keys:
                secrets_json[secret_type][endpoint][dict_key][key] = 0
    secrets_json["last_update"] = time.time()
    post_secrets(secrets_json)
    return

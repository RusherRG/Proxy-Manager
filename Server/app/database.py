from pymongo import MongoClient
import os

mongo_uri = 'mongodb://{0}:{1}'.format(
    "os.environ['mongo_user']", "os.environ['mongo_pass']")


def connect():
    """
    Create a connection to database
    """
    client = MongoClient(mongo_uri)
    db = client.distributed_requests
    return db


def add_request(request_json):
    """
    Add a request to database
    """
    db = connect().requests
    try:
        db.insert(request_json)
        return True
    except:
        return False

from pymongo import MongoClient
import os

MONGODB_HOST = os.environ['MONGODB_HOST']
MONGODB_PORT = int(os.environ['MONGODB_PORT'])


def connect():
    """
    Create a connection to database
    """
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
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
    except Exception as exc:
        print(exc)
        return False


def get_requests():
    """
    Get all requests from the database
    """
    db = connect().requests
    try:
        requests_list = list(db.find())
        for req in requests_list:
            del req['_id']
        # print(requests_list)
        return requests_list
    except Exception as err:
        print(err)
        return []

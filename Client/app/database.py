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


def get_requests():
    """
    Get all requests from the database
    """
    db = connect().requests
    try:
        requests_list = db.find()
        response = []
        for req in requests_list:
            del req['_id']
            response.append(req)
        return response
    except Exception as exc:
        print(exc)
        return []

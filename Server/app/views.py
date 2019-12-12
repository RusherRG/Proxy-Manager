from flask import render_template, request, jsonify
import time

from .database import add_request
from app import app


@app.route('/requests', methods=['POST'])
def requests():
    request_json = request.get_json()
    request_json['ip'] = request.remote_addr
    # add_request(request_json)
    print(request_json)
    process(request_json['value'])
    return jsonify({'status': True, 'id': request_json['id']})

def process(value):
    for _ in range(value):
        time.sleep(1)
    return

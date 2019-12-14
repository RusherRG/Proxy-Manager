from flask import render_template, request, jsonify
import time

from .database import add_request, get_requests
from app import app


@app.route('/requests', methods=['POST'])
def requests():
    request_json = request.get_json()
    request_json['ip'] = request.remote_addr
    result = add_request(request_json)
    print(result, request_json)
    process(request_json['value'])
    return jsonify({'status': True, 'id': request_json['id']})


def process(value):
    for _ in range(value):
        time.sleep(1)
    return


@app.route('/dashboard')
def dashboard():
    requests_list = get_requests()
    return render_template('dashboard.html', requests_list=requests_list)
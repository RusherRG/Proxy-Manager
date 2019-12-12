from flask import render_template, request, jsonify

from app import app


@app.route('/fetch_requests')
def fetch_requests():
    request_json = request.get_json()
    request_json['ip'] = request.remote_addr
    print(request_json)
    return render_template("dashboard.html")

from flask import render_template, request, jsonify

from app import app


@app.route('/')
def dashboard():
    print(request.remote_addr)
    return render_template("dashboard.html")


@app.route('/generate_request')
def generate_request():
    """
        Returns the request JSON
        Template:
        {
            "type": "GET", "POST", "DELETE"...
            "url": "http://www.google.com"
            "data": {
                request data
            }
        }
    """
    request_json = {
        "type": "POST",
        "url": "",
        "data": {}
    }
    return jsonify(request_json)

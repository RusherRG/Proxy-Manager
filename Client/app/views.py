from flask import render_template, request, jsonify
import random

from app import app
 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_request')
def generate_request():
    """
        Returns the request JSON
        Template:
        {
            "type": "GET", "POST", "DELETE"...
            "url": "http://www.google.com"
            "value": integer
        }
    """
    request_json = {
        "type": "POST",
        "url": "http://localhost:8000/requests",
        "value": random.randint(3, 7)
    }
    return jsonify(request_json)

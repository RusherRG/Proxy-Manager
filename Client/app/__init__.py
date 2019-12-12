from flask import Flask
from flask_cors import CORS

# Initialize the app
app = Flask(__name__, static_url_path="/static", instance_relative_config=True)
CORS(app)

# Load the views
from app import views

# Load the config file
app.config.from_object('config')

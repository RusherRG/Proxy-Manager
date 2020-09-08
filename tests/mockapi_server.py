from flask import Flask, request, jsonify
from utils import get_logger

app = Flask(__name__)
logger = get_logger(__name__)

LIMIT = 10

stats = {
    "api": {},
    "proxy": {}
}


@app.route("/api", methods=["GET"])
def api():
    headers = request.headers
    key = headers.get("key")
    logger.info("Received request at /api with key: {}".format(key))
    stats["api"][key] = stats["api"].get(key, 0) + 1
    if stats["api"][key] > LIMIT:
        message = "Limit Reached. Try again later."
    else:
        message = \
            "API limit is {}. {} requests used for key: {}".format(
                LIMIT, stats["api"][key], key)
    return jsonify({"message": message, "data": dict(request.args)})


@app.route("/proxy", methods=["POST"])
def proxy():
    ip = request.remote_addr
    stats["proxy"][ip] = stats["proxy"].get(ip, 0) + 1
    logger.info("Received request at /proxy with ip: {}".format(ip))
    if stats["proxy"][ip] > LIMIT:
        message = "Limit Reached. Try again later."
    else:
        message = "{} requests used for IP: {}".format(stats["proxy"][ip], ip)
    print()
    return jsonify({"message": message, "data": dict(request.form)})

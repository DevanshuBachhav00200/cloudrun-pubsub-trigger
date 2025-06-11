from flask import Flask, request
import os
from google.cloud import pubsub_v1
import json

app = Flask(__name__)
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv("GCP_PROJECT"), os.getenv("TOPIC_NAME"))

@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        return "Bad Request", 400

    name = envelope['name']
    size = envelope['size']
    content_type = envelope['contentType']

    message = {
        "filename": name,
        "size": size,
        "format": content_type
    }

    publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
    print(f"Published message: {message}")
    return "OK", 200

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask import request
import subprocess
import threading
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import signal
import os
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/api/segmentation', methods=['POST'])
def get_segmentation():
    data = request.get_json()

    image_url = data['image']
    x = data['x']
    y = data['y']
    selected_class = data['class']

    # Convert the image URL to a PIL image
    image_data = base64.b64decode(image_url.split(",")[-1])
    image = Image.open(io.BytesIO(image_data))

    # Process the image, x, y, and selected_class to get the segmentation mask
    mask = process_image(image, x, y, selected_class)

    # Convert the mask to a JSON object and return it
    mask_data = mask.tolist()
    return jsonify(mask_data)

def process_image(image, x, y, selected_class):
    # Your image processing and segmentation logic here

    # For demonstration purposes, we create a dummy mask of the same size as the image
    dummy_mask = np.zeros((image.height, image.width), dtype=np.uint8)

    # Return the mask (replace this with your actual mask)
    return dummy_mask

if __name__ == '__main__':
    socketio.run(app, debug=True)

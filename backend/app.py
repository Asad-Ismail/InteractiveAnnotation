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
import base64
from flask import Flask, request, jsonify
import base64
import io
from PIL import Image
import numpy as np
import logging
import cv2
from run_torch_inference import *

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

image=None

@app.route("/api/load_image", methods=["POST"])
def load_image():
    data = request.json
    global image
    logging.info(f"Loading Image")
    image_data = data["image"].split(",")[1]
    image = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image))
    return jsonify({"success": True})

@app.route('/api/segmentation', methods=['POST'])
def get_segmentation():
    logging.info(f"Received segmentation request kkk")
    if image is None:
        logging.info(f"Image is None")
        return jsonify({"Success": False, "Message": "No image loaded"})
    img=image.copy()
    data = request.get_json()
    #image_url = data['image']
    x = data['x']
    y = data['y']
    selected_class = data['class']
    logging.info(f"Received parameters: x={x}, y={y}, class={selected_class}")         
    # Convert the image URL to a PIL image
    #image_data = base64.b64decode(image_url.split(",")[-1])
    #image = Image.open(io.BytesIO(image_data))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # Save the image in a different format (e.g., PNG)
    point_color = (0, 0, 255)  # Red color in BGR
    # Draw the point
    radius = 15  # Radius of the point
    thickness = -1  # Thickness of the point (-1 indicates a filled circle)
    vis_img=cv2.circle(img.copy(), (x, y), radius, point_color, thickness)
    # Save the modified image
    cv2.imwrite("images/test.png", vis_img)

    # Process the image, x, y, and selected_class to get the segmentation mask
    mask = process_image_continuous(img, x, y, selected_class)
    mask=mask.squeeze(0)
    #print(f"Image shape is {img.shape}")
    #print(f"Mask shape is {mask.shape}")
    # Add these lines for debugging
    if not mask.any():
        print("Warning: mask is empty")
    else:
        print("Returning a non-empty mask")
    # Convert the mask to a JSON object and return it
    mask_data = mask.tolist()
    return jsonify(mask_data)

@app.route('/api/annotation', methods=['POST'])
def get_annotation():
    logging.info(f"Received segmentation request kkk")
    if image is None:
        logging.info(f"Image is None")
        return jsonify({"Success": False, "Message": "No image loaded"})
    img=image.copy()
    data = request.get_json()
    #image_url = data['image']
    x = data['x']
    y = data['y']
    selected_class = data['class']
    logging.info(f"Received parameters: x={x}, y={y}, class={selected_class}")         
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # Save the image in a different format (e.g., PNG)
    point_color = (0, 0, 255)  # Red color in BGR
    # Draw the point
    radius = 15  # Radius of the point
    thickness = -1  # Thickness of the point (-1 indicates a filled circle)
    vis_img=cv2.circle(img.copy(), (x, y), radius, point_color, thickness)
    # Save the modified image
    cv2.imwrite("images/test.png", vis_img)

    # Process the image, x, y, and selected_class to get the segmentation mask
    mask = process_image_continuous(img, x, y, selected_class)
    mask=mask.squeeze(0)
    #print(f"Image shape is {img.shape}")
    #print(f"Mask shape is {mask.shape}")
    # Add these lines for debugging
    if not mask.any():
        print("Warning: mask is empty")
    else:
        print("Returning a non-empty mask")
    # Convert the mask to a JSON object and return it
    mask_data = mask.tolist()
    return jsonify(mask_data)

def process_image_continuous(image, x, y, selected_class):
    # Your image processing and segmentation logic here
    height, width, channels = image.shape
    # For demonstration purposes, we create a dummy mask of the same size as the image
    #dummy_mask = np.zeros((height, width), dtype=np.uint8)
    mask=get_mask(image,[[x,y]],[1])
    # Return the mask (replace this with your actual mask)
    return mask

if __name__ == '__main__':
    socketio.run(app, debug=True)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import request
import logging
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

# Start with No image
image=None

def vis_point(img,x,y):
    # Save the image in a different format (e.g., PNG)
    point_color = (0, 0, 255)  # Red color in BGR
    # Draw the point
    radius = 15  # Radius of the point
    thickness = -1  # Thickness of the point (-1 indicates a filled circle)
    vis_img=cv2.circle(img.copy(), (x, y), radius, point_color, thickness)
    # Save the modified image
    cv2.imwrite("images/test.png", vis_img)
    
def vis_point(img,xs,ys):
    # Save the image in a different format (e.g., PNG)
    point_color = (0, 0, 255)  # Red color in BGR
    # Draw the point
    radius = 15  # Radius of the point
    thickness = -1  # Thickness of the point (-1 indicates a filled circle)
    for x,y in zip(xs,ys):
        vis_img=cv2.circle(img.copy(), (x, y), radius, point_color, thickness)
    # Save the modified image
    cv2.imwrite("images/test_click.png", vis_img)

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
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # Process the image, x, y, and selected_class to get the segmentation mask
    mask = process_image_continuous(img, x, y, selected_class)
    mask=mask.squeeze(0)
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
    results = request.get_json()
    annotations=results["annotations"]
    if "save_res" in results:
        save_res=True
        logging.info(f"Saving initiated!!")
    else:
        save_res=False
    xs=[]
    ys=[]
    s_classes=[]
    labels=[]
    for annotation in annotations:
        xs.append(annotation['x'])
        ys.append(annotation['y'])
        s_classes.append(annotation['class'])
        labels.append(annotation['label'])
        
    logging.info(f"Received parameters: x={xs}, y={ys}, class={s_classes}, label ={labels}")       
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # Process the image, x, y, and selected_class to get the segmentation mask
    mask = process_image_batch(img, xs, ys, labels)
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
    mask=get_mask(image,[[x,y]],[1])
    # Return the mask (replace this with your actual mask)
    return mask

def process_image_batch(image, xs, ys,labels):
    height, width, channels = image.shape
    mask=get_mask(image,list(zip(xs,ys)),labels)
    # Return the mask (replace this with your actual mask)
    return mask

if __name__ == '__main__':
    socketio.run(app, debug=True)

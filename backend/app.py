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
import pycocotools.mask as mask_util
import json
import os
# Model is initialized here
#from run_torch_inference import *
from run_onnx_inference import *

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Start with No image
image=None
filename=None
annotations=[]
annotation_id = 0 
saved_masks = {}  # Save masks per class

def encode_mask_to_coco_rle(mask):
    rle = mask_util.encode(np.asfortranarray(mask.astype(np.uint8)))
    rle['counts'] = rle['counts'].decode('utf-8')  # Add this line to decode the 'counts' field
    return rle

def decode_coco_rle_to_mask(rle):
    h, w = rle['size']  # Extract height and width from the RLE object
    rle['counts'] = rle['counts'].encode('utf-8')  # Encode the 'counts' field back to bytes
    mask = mask_util.decode(rle)  # Decode the RLE mask
    mask = np.array(mask, dtype=np.uint8)  # Convert the mask to a NumPy array
    return mask.reshape(h, w)  # Reshape the mask to its original dimensions (height and width)

def compute_bbox(mask):
    y_indices, x_indices = np.where(mask)
    x_min, x_max = x_indices.min(), x_indices.max()
    y_min, y_max = y_indices.min(), y_indices.max()
    width = x_max - x_min
    height = y_max - y_min
    return [float(x_min), float(y_min), float(width), float(height)]

def vis_point(img,x,y):
    # Save the image in a different format (e.g., PNG)
    point_color = (0, 0, 255)  # Red color in BGR
    # Draw the point
    radius = 15  # Radius of the point
    thickness = -1  # Thickness of the point (-1 indicates a filled circle)
    vis_img=cv2.circle(img.copy(), (x, y), radius, point_color, thickness)
    # Save the modified image
    cv2.imwrite("images/test.png", vis_img)
    
def vis_points(img,xs,ys):
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
    global annotations
    global annotation_id
    global filename
    global saved_masks
    
    logging.info(f"Loading Image!!")
    image_data = data["image"].split(",")[1]
    filename = data["filename"]
    #logging.info(f"Passed Filename is {filename}")
    image = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image))
    set_image(image)
    # reset annotations
    annotations = []
    annotation_id = 0  # Changed from annotaiton_id
    saved_masks={}
    return jsonify({"success": True})

@app.route('/api/segmentation', methods=['POST'])
def get_segmentation():
    logging.info(f"Received Preview segmentation request")
    # Resetting saved_mask for preview mode
    saved_masks = {} 
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
    vis_point(img,x,y)
    mask = process_image_continuous(img, x, y, selected_class)
    mask=mask.squeeze(0)
    if not mask.any():
        print("Warning: mask is empty")
    else:
        print("Returning a non-empty mask") 
    # Save the current mask with the class
    current_class = "Stuff"
    saved_masks_data = {}
    current_mask= {current_class:mask.tolist()}
    response_data = {
        #"combined_mask": combined_mask.tolist(),
        "saved_masks": saved_masks_data,
        "current_mask": current_mask
    }
    return jsonify(response_data)
        
@app.route('/api/save_annotation', methods=['POST'])
def save_annotation():
    global annotations
    global filename
    inputs = request.get_json()
    logging.info(f"Saving initiated!!")
    # if save_res is passed must also have output_path
    output_path=inputs["output_path"]
    #logging.warn(f"Annotations are {annotations}")
    json_file="".join(filename.split(".")[:-1])
    pth=os.path.join(output_path,json_file+".json")
    logging.info(f"Output path is {pth}")
    #reset_low_res()
    with open(pth, "w") as f:
        json.dump(annotations, f)
    return jsonify({"message": "Annotation saved successfully"}), 200

@app.route('/api/annotation', methods=['POST'])
def get_annotation():
    #logging.info(f"Received segmentation request")
    global annotation_id
    global annotations
    global saved_masks
    
    if image is None:
        logging.info(f"Image is None")
        return jsonify({"Success": False, "Message": "No image loaded"})
    img=image.copy()
    inputs = request.get_json()
    anns=inputs["annotations"]
    output_path=None
    if "done_obj" in inputs:
        done_obj=True
        logging.info(f"Done Object!!")
    else:
        done_obj=False
    xs=[]
    ys=[]
    s_classes=[]
    labels=[]
    for annotation in anns:
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
    
    # Save the current mask with the class
    current_class = s_classes[-1]
    
    if done_obj:
        # Create an annotation in COCO format
        bbox = compute_bbox(mask)
        annotation = {
            "id": annotation_id,
            "image_name": 1,
            "category_id": s_classes[-1],
            "segmentation": encode_mask_to_coco_rle(mask),
            "area": float(mask.sum()),
            "bbox": bbox,
            "iscrowd": 0
        }
        annotations.append(annotation)
        annotation_id += 1
        if current_class not in saved_masks:
            saved_masks[current_class] = mask
        else:
            saved_masks[current_class] = np.logical_or(saved_masks[current_class], mask)
    
    saved_masks_data = {key: mask.tolist() for key, mask in saved_masks.items()}
    current_mask= {current_class:mask.tolist()}
    response_data = {
        #"combined_mask": combined_mask.tolist(),
        "saved_masks": saved_masks_data,
        "current_mask": current_mask
    }
    return jsonify(response_data)

def process_image_continuous(image, x, y, selected_class):
    #reset_low_res()
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

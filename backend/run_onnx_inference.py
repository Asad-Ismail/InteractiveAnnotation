from segment_anything.utils.onnx import SamOnnxModel
import onnxruntime
from segment_anything import sam_model_registry, SamPredictor
import matplotlib.pyplot as plt
import numpy as np
import cv2


def show_mask(mask, ax):
    color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))   
    


checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
sam = sam_model_registry[model_type](checkpoint=checkpoint)

onnx_model_path='sam_onnx_vit_h.onnx'
ort_session = onnxruntime.InferenceSession(onnx_model_path)
sam.to(device='cuda')
predictor = SamPredictor(sam)

image_embedding=None
low_res_masks=None


def reset_low_res():
    global low_res_masks
    low_res_masks=None

def set_image(image):
    global image_embedding
    global low_res_masks
    print(f"Setting Image in model!")
    # Reset low res masks
    low_res_masks=None
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    predictor.set_image(image)
    image_embedding = predictor.get_image_embedding().cpu().numpy()

def get_mask(image,point,label):
    global image_embedding
    global low_res_masks
    onnx_coord = np.concatenate([point, np.array([[0.0, 0.0]])], axis=0)[None, :, :]
    onnx_label = np.concatenate([label, np.array([-1])], axis=0)[None, :].astype(np.float32)
    onnx_coord = predictor.transform.apply_coords(onnx_coord, image.shape[:2]).astype(np.float32)
    if low_res_masks:
        onnx_mask_input = low_res_masks
        onnx_has_mask_input = np.ones(1, dtype=np.float32)
    else:
        onnx_mask_input = np.zeros((1, 1, 256, 256), dtype=np.float32)
        onnx_has_mask_input = np.zeros(1, dtype=np.float32)
    ort_inputs = {
    "image_embeddings": image_embedding,
    "point_coords": onnx_coord,
    "point_labels": onnx_label,
    "mask_input": onnx_mask_input,
    "has_mask_input": onnx_has_mask_input,
    "orig_im_size": np.array(image.shape[:2], dtype=np.float32)
    }
    masks, probs, low_res_logits = ort_session.run(None, ort_inputs)
    low_res_masks=low_res_logits
    masks = masks > predictor.model.mask_threshold
    max_prob=np.argmax(probs)
    mask=masks[max_prob]
    return mask
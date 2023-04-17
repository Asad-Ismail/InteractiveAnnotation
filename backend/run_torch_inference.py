import torch
import torchvision
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
import sys
from segment_anything import sam_model_registry, SamPredictor
print("PyTorch version:", torch.__version__)
print("Torchvision version:", torchvision.__version__)
print("CUDA is available:", torch.cuda.is_available())

def show_mask(mask, ax=None, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    
    if ax:
        ax.imshow(mask_image)
    else:
        cv2.imwrite("images/mask.png", (mask_image*255).astype(np.uint8))
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2)) 

sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cuda"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
print(f"Loaded SAM model from {sam_checkpoint}!")
predictor = SamPredictor(sam)    

def get_mask(image,point,label):
    predictor.set_image(image)
    input_point = np.array(point).reshape(-1,2)
    input_label = np.array(label)
    print(f"Running Inference!")
    masks, _, _ = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=False,)
    print(f"Finished Forward path!")
    #show_mask(masks)
    return masks

if __name__=="__main__":
    image_path = 'images/truck.jpg'
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    point = [[500, 375]]
    label = [1]
    masks = get_mask(image,point,label)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.imshow(image)
    show_mask(masks[0], ax, random_color=True)
    plt.show()
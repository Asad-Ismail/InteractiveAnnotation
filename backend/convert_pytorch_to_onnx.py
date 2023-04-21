import argparse
import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
import warnings
import onnxruntime
from onnxruntime.quantization import QuantType
from onnxruntime.quantization.quantize import quantize_dynamic
from segment_anything import sam_model_registry, SamPredictor
from segment_anything.utils.onnx import SamOnnxModel


def main(args):
    checkpoint = args.checkpoint
    model_type = args.model_type

    sam = sam_model_registry[model_type](checkpoint=checkpoint)

    onnx_model_path = args.onnx_model_path

    onnx_model = SamOnnxModel(sam, return_single_mask=True)

    dynamic_axes = {
        "point_coords": {1: "num_points"},
        "point_labels": {1: "num_points"},
    }

    embed_dim = sam.prompt_encoder.embed_dim
    embed_size = sam.prompt_encoder.image_embedding_size
    mask_input_size = [4 * x for x in embed_size]
    dummy_inputs = {
        "image_embeddings": torch.randn(1, embed_dim, *embed_size, dtype=torch.float),
        "point_coords": torch.randint(low=0, high=1024, size=(1, 5, 2), dtype=torch.float),
        "point_labels": torch.randint(low=0, high=4, size=(1, 5), dtype=torch.float),
        "mask_input": torch.randn(1, 1, *mask_input_size, dtype=torch.float),
        "has_mask_input": torch.tensor([1], dtype=torch.float),
        "orig_im_size": torch.tensor([1500, 2250], dtype=torch.float),
    }
    output_names = ["masks", "iou_predictions", "low_res_masks"]

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        with open(onnx_model_path, "wb") as f:
            torch.onnx.export(
                onnx_model,
                tuple(dummy_inputs.values()),
                f,
                export_params=True,
                verbose=False,
                opset_version=17,
                do_constant_folding=True,
                input_names=list(dummy_inputs.keys()),
                output_names=output_names,
                dynamic_axes=dynamic_axes,
            )

    print(f"ONNX path is {onnx_model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert SAM model to ONNX format.")
    parser.add_argument("--checkpoint", default="sam_vit_h_4b8939.pth", help="Path to the checkpoint file.")
    parser.add_argument("--model_type", default="vit_h", help="Type of SAM model.")
    parser.add_argument("--onnx_model_path", default="sam_onnx_vit_h.onnx", help="Output path for the ONNX model.")
    args = parser.parse_args()
    main(args)

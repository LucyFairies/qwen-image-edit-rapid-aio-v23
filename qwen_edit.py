#!/usr/bin/env python3
"""
Basic local image edit script for Qwen Image Edit Rapid AIO style models.
Tested/adapted for v23 and similar community merges.

Usage:
1. Install requirements (see requirements.txt)
2. Download the model (e.g. from Phr00t or your merged version)
3. python qwen_edit.py --image input.png --prompt "edit description here" --output edited.png

For the "Rapid AIO" (4-step) versions, the model is usually a merged checkpoint that works with standard pipelines or ComfyUI.

Adjust model_id or local path as needed.
"""

import os
# Prefer D: cache for large HF models if available (huggingface_hub)
if os.path.exists("D:\\"):
    os.environ.setdefault("HUGGINGFACE_HUB_CACHE", r"D:\hf-cache")

import argparse
import torch
from diffusers import QwenImageEditPipeline  # Base; for AIO merges you may load custom unet/vae/clip
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description="Qwen Image Edit (Rapid AIO style)")
    parser.add_argument("--image", type=str, required=True, help="Path to input image")
    parser.add_argument("--prompt", type=str, required=True, help="Editing prompt / instruction")
    parser.add_argument("--output", type=str, default="edited.png", help="Output path")
    parser.add_argument("--model", type=str, default="Qwen/Qwen-Image-Edit-2511", help="HF model id or local path to checkpoint")
    parser.add_argument("--steps", type=int, default=4, help="Inference steps (4 for rapid)")
    parser.add_argument("--guidance", type=float, default=1.0, help="Guidance scale (often ~1 for rapid)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--dtype", type=str, default="float16", choices=["float16", "bfloat16", "float32"])
    args = parser.parse_args()

    print(f"Loading model: {args.model}")
    dtype = getattr(torch, args.dtype)

    # For standard Qwen Image Edit:
    # Some Rapid AIO versions are distributed as full pipeline or as separate components.
    # If you have a safetensors AIO checkpoint for ComfyUI-style, you may need a custom loader.
    # This example uses the base pipeline; adapt for your merged checkpoint.

    pipe = QwenImageEditPipeline.from_pretrained(
        args.model,
        torch_dtype=dtype,
    ).to(args.device)

    # Optional: enable memory optimizations
    if hasattr(pipe, "enable_model_cpu_offload"):
        pipe.enable_model_cpu_offload()
    if hasattr(pipe, "enable_vae_slicing"):
        pipe.enable_vae_slicing()

    print(f"Loading input image: {args.image}")
    image = Image.open(args.image).convert("RGB")

    generator = None
    if args.seed is not None:
        generator = torch.Generator(device=args.device).manual_seed(args.seed)

    print(f"Running edit: steps={args.steps}, guidance={args.guidance}")
    result = pipe(
        prompt=args.prompt,
        image=image,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance,
        generator=generator,
    ).images[0]

    result.save(args.output)
    print(f"Saved edited image to {args.output}")

if __name__ == "__main__":
    main()

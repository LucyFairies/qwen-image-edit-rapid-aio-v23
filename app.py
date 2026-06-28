#!/usr/bin/env python3
"""
Simple local Gradio app for Qwen Image Edit Rapid AIO (v23 style).

Run: python app.py
Then open the local URL.

This is a starter to replicate / extend your HF Space locally.
For production use the full merged checkpoint and any custom pipeline your space uses.

Requirements: see requirements.txt + gradio
"""

import os
# Prefer D: cache for large HF models if available (huggingface_hub)
if os.path.exists("D:\\"):
    os.environ.setdefault("HUGGINGFACE_HUB_CACHE", r"D:\hf-cache")

import gradio as gr
import torch
from diffusers import QwenImageEditPipeline
from PIL import Image
from datetime import datetime

# Change this to your local path or the HF id of your v23 merge
MODEL_ID = os.environ.get("QWEN_MODEL", "Qwen/Qwen-Image-Edit-2511")

# Output directory preference: D: drive if available (for large outputs)
if os.path.exists("D:\\"):
    OUTPUT_DIR = r"D:\qwen-edits"
else:
    OUTPUT_DIR = os.path.join(os.getcwd(), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Outputs will be saved to: {OUTPUT_DIR}")

print("Loading pipeline (this may take time on first run)...")
pipe = QwenImageEditPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)
if torch.cuda.is_available():
    pipe = pipe.to("cuda")
    try:
        pipe.enable_model_cpu_offload()
    except Exception:
        pass

def edit_image(image: Image.Image, prompt: str, steps: int = 4, guidance: float = 1.0, seed: int = -1):
    if image is None:
        return None, "Please upload an image."
    if not prompt or not prompt.strip():
        return None, "Please provide an edit prompt."

    generator = None
    if seed is not None and seed >= 0:
        generator = torch.Generator(device=pipe.device).manual_seed(int(seed))

    result = pipe(
        prompt=prompt,
        image=image.convert("RGB"),
        num_inference_steps=int(steps),
        guidance_scale=float(guidance),
        generator=generator,
    ).images[0]

    # Save to D:\qwen-edits (or fallback) with timestamp + sanitized prompt
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c for c in (prompt or "result")[:50] if c.isalnum() or c in " -_").strip().replace(" ", "_") or "edit"
    filename = f"qwen_{ts}_{safe}.png"
    save_path = os.path.join(OUTPUT_DIR, filename)
    result.save(save_path)
    print(f"Saved edited image to: {save_path}")

    return result, f"Edit complete. Saved to: {save_path}"

with gr.Blocks(title="Qwen Image Edit Rapid AIO v23 (Local)") as demo:
    gr.Markdown("# Qwen Image Edit Rapid AIO v23 - Local Demo")
    gr.Markdown("Fast image editing (4-step rapid style). Outputs are automatically saved to **D:\\qwen-edits** (if available) or ./outputs. Tune steps/guidance for your merge.")

    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Input Image")
            prompt = gr.Textbox(label="Edit Prompt / Instruction", placeholder="e.g. change the background to a cyberpunk city, keep the person")
            steps = gr.Slider(1, 20, value=4, step=1, label="Inference Steps (4 recommended for rapid)")
            guidance = gr.Slider(0.0, 7.5, value=1.0, step=0.1, label="Guidance Scale (often ~1.0)")
            seed = gr.Number(value=-1, label="Seed (-1 = random)", precision=0)
            run_btn = gr.Button("Edit Image", variant="primary")

        with gr.Column():
            output_image = gr.Image(type="pil", label="Result")
            status = gr.Textbox(label="Status")

    run_btn.click(
        fn=edit_image,
        inputs=[input_image, prompt, steps, guidance, seed],
        outputs=[output_image, status]
    )

    gr.Examples(
        examples=[
            ["https://huggingface.co/datasets/hf-internal-testing/diffusers-images/resolve/main/image_to_image/cat.png", "make it a cyberpunk cat with neon lights"],
        ],
        inputs=[input_image, prompt]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

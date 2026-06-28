# qwen-image-edit-rapid-aio-v23

**GitHub:** https://github.com/LucyFairies/qwen-image-edit-rapid-aio-v23

Hugging Face Space by h4sch for **Qwen Image Edit Rapid AIO v23** (NSFW capable).

**Space URL:** https://huggingface.co/spaces/h4sch/qwen-image-edit-rapid-aio-v23

This is a fast, all-in-one (AIO) setup for the Qwen Image Edit model (based on Qwen/Qwen-Image-Edit-2511 and community merges like Phr00t's Rapid AIO series).

## Key Features (from community)
- **Rapid inference**: Typically 4 steps (Lightning LoRA style), CFG=1, very fast.
- **Image-to-Image editing** with strong prompt adherence (v23 tuned for this).
- **Text-to-Image** support as well.
- NSFW friendly in appropriate versions.
- Merged VAE + CLIP + accelerators for easy one-click use (especially in ComfyUI).

## Local Setup (Windows + this env)

**Status (2026-06-28):** CUDA-ready. Torch 2.6.0+cu124 + torchvision/torchaudio + diffusers/gradio installed and verified in `C:\Users\h4sch\env` on RTX 3050 (8 GB VRAM). See verification below.

### Verified environment
```powershell
# From this dir
& "C:\Users\h4sch\env\Scripts\python.exe" -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

### Install / Repair (if needed later)
```powershell
cd C:\Users\h4sch

# Torch CUDA 12.4 (match your driver)
.\env\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Rest of deps
.\env\Scripts\python.exe -m pip install -r workdir/qwen-image-edit-rapid-aio-v23/requirements.txt
```

Note: The `~ympy` pip warning (if any) is cosmetic from earlier partial uninstall; safe to ignore.

### Model notes for v23 Rapid AIO

- The scripts here (`app.py`, `qwen_edit.py`) default to the **base** `Qwen/Qwen-Image-Edit-2511` via `QwenImageEditPipeline`. This is a working diffusers path.
- For the full **Phr00t Rapid AIO v23** (especially the NSFW/SFW .safetensors merges): primarily designed for **ComfyUI** (merged VAE+CLIP+UNet checkpoint). See [COMFYUI.md](./COMFYUI.md).
- To point scripts to another model: set env var `QWEN_MODEL=...` or edit `--model` / `MODEL_ID`.
- First run of scripts will download model weights (several GB) to your HF cache. Disk + time required.

**Typical rapid settings (v23 style):** `--steps 4 --guidance 1.0` (or CFG 1.0 in Comfy).

For ComfyUI users (very popular for this model):
- Load as unet + clip + vae in the AIO checkpoint.
- Use 4 steps, low CFG.

## Basic Local Script (Diffusers)

See `qwen_edit.py` in this folder for a starter script.

## ComfyUI Workflow

Many users use ComfyUI with this model for best control.

Recommended:
- Use the "Qwen Image Edit" custom nodes if available.
- Or standard load checkpoint + IPAdapter or direct conditioning for edit.
- Search for "Qwen Image Edit Rapid AIO ComfyUI" workflows (there are good ones on GitHub and Civitai).

## Project Notes

- This project/space is for fast, high-quality image editing.
- v23 emphasizes prompt adherence.
- For best results with multi-image or complex scenes, test different versions (community notes v19 for consistency, v23 for adherence).
- NSFW versions exist in the ecosystem.

## Quick Start (CUDA env ready)

Test image ready: `test_input.png`

### Gradio UI (empfohlen zum Testen)
```powershell
cd C:\Users\h4sch\workdir\qwen-image-edit-rapid-aio-v23
& "C:\Users\h4sch\env\Scripts\python.exe" app.py
```
Öffne http://localhost:7860

### CLI
```powershell
& "C:\Users\h4sch\env\Scripts\python.exe" qwen_edit.py `
  --image test_input.png `
  --prompt "add sunglasses, cyberpunk neon lighting, keep subject" `
  --steps 4 `
  --guidance 1.0 `
  --output edited.png
```

**Wichtig beim ersten Lauf:** Das Modell (Qwen/Qwen-Image-Edit-2511 oder anderes) wird heruntergeladen (mehrere GB). Danach cached. Bei 8 GB VRAM nutzt der Code CPU-Offload — bei OOM ggf. `--dtype float16` oder sequentielles Offload ausprobieren / Auflösung reduzieren.

## Next Steps / Ideas

- Local Gradio mirror of the Space (done).
- ComfyUI custom node or workflow export.
- Integration with local image tools / batch editing.
- Optimization for specific hardware (e.g. the user's setup).

Clone or contribute to related:
- Main community model: https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO

Run the local script or install ComfyUI for best experience.

---
Maintained as local mirror / dev area for h4sch's HF Space.
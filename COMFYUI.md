# ComfyUI Usage for Qwen Image Edit Rapid AIO v23

This model is very popular in the ComfyUI community because of its speed (4-step / Lightning style).

## Recommended Setup

1. Install ComfyUI (latest).
2. Download the appropriate checkpoint for v23:
   - Look for safetensors AIO versions or GGUF quants (search "Qwen-Image-Edit-Rapid-AIO v23 GGUF" or similar on HF/Civitai).
3. Place files:
   - unet / checkpoint → `ComfyUI/models/unet/`
   - vae (if separate) → `ComfyUI/models/vae/`
   - clip / text encoders → `ComfyUI/models/clip/`

4. Use or adapt existing workflows:
   - Search GitHub / Civitai / Reddit for "Qwen Image Edit Rapid AIO ComfyUI"
   - Common nodes: Load Checkpoint, CLIP Text Encode, VAE Decode, KSampler (with low steps), IPAdapter or direct image conditioning for edit.

## Typical Settings for Rapid Versions

- Steps: 4 (or 1-8)
- CFG: 1.0
- Sampler: euler_ancestral or beta (as recommended in model cards)
- Scheduler: simple or beta

## Multi-image / Reference Images

For scenes with multiple subjects or reference images, v23 focuses on prompt adherence but may need careful prompting or additional conditioning (IPAdapter, ControlNets, etc.).

## NSFW Note

Use the NSFW-tuned merges if available for your version. Your HF Space is marked NSFW.

## Tips

- Start with a good base image.
- Be specific in the prompt (subject, style, lighting, changes).
- For consistency across edits, some users prefer earlier versions (e.g. v19); v23 is stronger on following complex prompts.

If you have a specific workflow json from your Space, drop it here and we can adapt it or improve it.

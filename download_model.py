#!/usr/bin/env python3
"""
Clean model download using huggingface_hub.
Saves to D:\hf-cache (if available) for large model storage.
Run this to pre-download before starting the Gradio app.
"""

import os
import sys

# Prefer D: drive for cache if it exists (as per user preference)
if os.path.exists("D:\\"):
    cache_dir = r"D:\hf-cache"
    os.makedirs(cache_dir, exist_ok=True)
    os.environ["HUGGINGFACE_HUB_CACHE"] = cache_dir
    print(f"Using cache on D: {cache_dir}")
else:
    print("D: not found, using default cache")

from huggingface_hub import snapshot_download

MODEL_ID = "Qwen/Qwen-Image-Edit-2511"

print(f"\n=== Downloading {MODEL_ID} with huggingface_hub ===")
print("This will show progress and resume if interrupted.\n")

try:
    local_path = snapshot_download(
        repo_id=MODEL_ID,
        resume_download=True,
    )
    print(f"\n✅ Download complete!")
    print(f"Model cached at: {local_path}")
    print("\nYou can now run the app (it will use the cached files):")
    print('  $env:HUGGINGFACE_HUB_CACHE = "D:\\hf-cache"; & "C:\\Users\\h4sch\\env\\Scripts\\python.exe" app.py')
except Exception as e:
    print(f"\n❌ Download error: {e}")
    sys.exit(1)

input("\nPress Enter to close this window...")

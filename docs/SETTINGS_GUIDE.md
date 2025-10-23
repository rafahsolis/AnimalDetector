# Simple-Settings Configuration Guide

## Overview

Your Animal Detector project now uses `python-simple-settings` for clean configuration management.

## How It Works

### 1. Settings Hierarchy

Settings are loaded in this order (later overrides earlier):
1. `settings.py` - Default/production settings
2. `settings_local.py` - Your local overrides (gitignored)

### 2. Key Settings

#### GPU Configuration
```python
DEVICE = "0"  # "0" for GPU, "cpu" for CPU
```

#### Model Selection
```python
MODEL_PATH = "yolov11l.pt"  # YOLOv11 Large (best accuracy)
# Alternatives:
# MODEL_PATH = "yolov8n.pt"  # Fastest, less accurate
# MODEL_PATH = "yolov8m.pt"  # Balanced
```

#### Detection Parameters
```python
DETECTION_CONFIDENCE_THRESHOLD = 0.25  # 0.0 to 1.0
VERBOSE_OUTPUT = True  # Enable detailed logging
```

#### Paths
```python
IMAGE_FOLDER = Path("/mnt/nextcloud/TrailCams")
LOG_FILE = BASE_DIR / "detections.csv"
```

## Customizing Settings

### For Local Development

Edit `settings_local.py`:
```python
# Enable verbose output for debugging
VERBOSE_OUTPUT = True

# Use a different image folder
from pathlib import Path
IMAGE_FOLDER = Path("/home/myuser/test_images")

# Lower confidence threshold to catch more detections
DETECTION_CONFIDENCE_THRESHOLD = 0.15
```

### For Production

Edit `settings.py` directly or set environment variables:
```bash
export SIMPLE_SETTINGS=settings,settings_production
```

## GPU Verification

The system automatically:
1. Checks if CUDA is available
2. Prints GPU information if `VERBOSE_OUTPUT = True`
3. Falls back to CPU if GPU unavailable

Run the test to verify:
```bash
python test_settings.py
```

## YOLO Model Recommendations

For animal detection on GPU:

| Model | Speed | Accuracy | GPU Memory | Best For |
|-------|-------|----------|------------|----------|
| yolov8n.pt | ⚡⚡⚡ | ⭐⭐ | Low | Real-time processing |
| yolov8m.pt | ⚡⚡ | ⭐⭐⭐ | Medium | Balanced use case |
| **yolov11l.pt** | ⚡ | ⭐⭐⭐⭐⭐ | High | **Best accuracy** ✓ |

Your current setting uses **YOLOv11 Large** - the best choice for accurate animal detection!

## Common Use Cases

### 1. Quick Test with Low Threshold
```python
# settings_local.py
DETECTION_CONFIDENCE_THRESHOLD = 0.1
IMAGE_FOLDER = Path("./test_images")
VERBOSE_OUTPUT = True
```

### 2. Production with High Accuracy
```python
# settings.py
DETECTION_CONFIDENCE_THRESHOLD = 0.5
MODEL_PATH = "yolov11l.pt"
VERBOSE_OUTPUT = False
```

### 3. CPU-Only Mode
```python
# settings_local.py
DEVICE = "cpu"
```

## Troubleshooting

### "Settings not found"
Ensure you run from project root:
```bash
cd /home/rafa/PycharmProjects/AnimalDetector
python main.py
```

### GPU Not Detected
Check PyTorch CUDA support:
```python
import torch
print(torch.cuda.is_available())
```

### Settings Not Loading
Verify the environment variable:
```python
import os
print(os.environ.get('SIMPLE_SETTINGS'))
```


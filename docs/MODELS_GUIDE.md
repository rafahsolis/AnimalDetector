# YOLO Models Guide

## Available Model Types

This project supports all YOLO models from both **YOLOv8** and **YOLO11** families.

### Model Sizes (from fastest to most accurate)

- **n (nano)** - Fastest, smallest, least accurate (~6-10 MB)
- **s (small)** - Fast, small, good accuracy (~20-25 MB)
- **m (medium)** - Balanced speed and accuracy (~40-50 MB)
- **l (large)** - Slower, large, high accuracy (~80-100 MB)
- **x (extra-large)** - Slowest, largest, highest accuracy (~130-150 MB)

### Task Types

1. **Detection** (default) - Standard object detection with bounding boxes
   - Files: `yolov8{n,s,m,l,x}.pt`, `yolo11{n,s,m,l,x}.pt`

2. **Segmentation** (-seg) - Instance segmentation with pixel masks
   - Files: `yolov8{n,s,m,l,x}-seg.pt`, `yolo11{n,s,m,l,x}-seg.pt`

3. **Pose Estimation** (-pose) - Human pose/keypoint detection
   - Files: `yolov8{n,s,m,l,x}-pose.pt`, `yolo11{n,s,m,l,x}-pose.pt`

4. **Classification** (-cls) - Image classification
   - Files: `yolov8{n,s,m,l,x}-cls.pt`, `yolo11{n,s,m,l,x}-cls.pt`

5. **Oriented Bounding Box** (-obb) - Rotated object detection
   - Files: `yolov8{n,s,m,l,x}-obb.pt`, `yolo11{n,s,m,l,x}-obb.pt`

## Total Available Models

- **50 detection models** (10 models: 5 v8 sizes + 5 v11 sizes)
- **10 segmentation models** (5 v8 sizes + 5 v11 sizes)
- **10 pose models** (5 v8 sizes + 5 v11 sizes)
- **10 classification models** (5 v8 sizes + 5 v11 sizes)
- **10 OBB models** (5 v8 sizes + 5 v11 sizes)

**Total: 50 models**

## Downloading Models

### Download all detection models (default)
```bash
python -m yolo.download_models
```

### Download specific model
```bash
python -m yolo.download_models yolov8m.pt
python -m yolo.download_models yolo11l-seg.pt
```

### Download by category
```bash
python -m yolo.download_models --detection        # All detection models
python -m yolo.download_models --segmentation     # All segmentation models
python -m yolo.download_models --pose             # All pose models
python -m yolo.download_models --classification   # All classification models
python -m yolo.download_models --obb              # All OBB models
python -m yolo.download_models --all              # ALL 50 models (warning: ~5GB+ total)
```

## Using Models in Code

### Basic Detection
```python
from pathlib import Path
from yolo import AnimalDetector

model_path = Path('yolo/models/yolo11m.pt')
detector = AnimalDetector(model_path, device='0', confidence_threshold=0.25)
detector.load_model()

detections = detector.detect_animals_in_image(image_path, target_animals=['dog', 'cat'])
```

### Model Registry
```python
from yolo import ModelRegistry, YoloModelVersion
from settings import MODELS_DIR

registry = ModelRegistry(MODELS_DIR)

# Get path for specific model
model_path = registry.get_model_path(YoloModelVersion.V11M)

# Check if model is available
if registry.is_model_available(YoloModelVersion.V11L_SEG):
    print("Segmentation model is ready!")

# List all downloaded models
available = registry.get_all_available_models()
print(f"Downloaded models: {list(available.keys())}")
```

## Recommendations

### For Animal Detection (this project):
- **Best balance**: `yolo11m.pt` or `yolov8m.pt`
- **Fastest**: `yolo11n.pt` or `yolov8n.pt`
- **Most accurate**: `yolo11x.pt` or `yolov8x.pt`

### Version Differences:
- **YOLO11** - Latest, slightly better accuracy and speed
- **YOLOv8** - Mature, well-tested, slightly larger models

### GPU Memory Requirements:
- **nano/small** - Can run on 2-4GB GPU
- **medium** - Needs 4-6GB GPU
- **large/extra-large** - Needs 6-8GB+ GPU

## Storage Requirements

If downloading all models:
- Detection models: ~500 MB
- Segmentation models: ~600 MB
- Pose models: ~550 MB
- Classification models: ~400 MB
- OBB models: ~550 MB
- **Total: ~2.6 GB**


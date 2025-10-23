# Animal Detector

Animal detection system using YOLO for detecting rabbits, foxes, wild boars, birds, and other animals using GPU acceleration.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your settings by creating a `settings_local.py` file (optional):
```python
# Override any settings from settings.py
DEVICE = "0"  # Use GPU
VERBOSE_OUTPUT = True
IMAGE_FOLDER = Path("/your/custom/path")
```

## Configuration

The project uses `python-simple-settings` for configuration management.

### Main Settings (`settings.py`)

- `DEVICE`: Device to use for inference ("0" for GPU, "cpu" for CPU)
- `MODEL_PATH`: Path to YOLO model weights (e.g., "yolov11l.pt")
- `IMAGE_FOLDER`: Path to folder containing images to process
- `LOG_FILE`: Path to output CSV file with detections
- `DETECTION_CONFIDENCE_THRESHOLD`: Minimum confidence for detections (0.0-1.0)
- `VERBOSE_OUTPUT`: Enable/disable verbose logging
- `TARGET_ANIMALS`: List of target animal species

### Local Settings (`settings_local.py`)

Create this file to override default settings without modifying `settings.py`.
This file is gitignored by default.

## Usage

Run the detection pipeline:
```bash
python main.py
```

Or run the yolo module directly:
```bash
python -m yolo.yolo
```

## GPU Support

The system automatically detects GPU availability and uses it if available.
To force CPU usage, set `DEVICE = "cpu"` in your settings.

### YOLO Versions

Higher YOLO versions generally perform better:
- **YOLOv8n**: Fastest, lowest accuracy (nano)
- **YOLOv8m**: Balanced (medium)
- **YOLOv11l**: Best accuracy, slower (large)

Set your preferred model in `settings.py`:
```python
MODEL_PATH = "yolov11l.pt"  # For best accuracy
```

## Project Structure

```
AnimalDetector/
├── main.py              # Main entry point
├── settings.py          # Default configuration
├── settings_local.py    # Local overrides (gitignored)
├── requirements.txt     # Python dependencies
├── yolo/
│   ├── __init__.py
│   └── yolo.py         # Detection logic
└── detections.csv      # Output file (generated)
```

## Training Custom Models

```python
from yolo.yolo import ModelTrainer
from simple_settings import settings

trainer = ModelTrainer(
    settings.DATASET_PATH,
    settings.MODEL_ARCHITECTURE,
    device=settings.DEVICE
)
trainer.train(
    epochs=settings.TRAINING_EPOCHS,
    imgsz=settings.TRAINING_IMAGE_SIZE
)
```


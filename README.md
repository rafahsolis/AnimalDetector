# Animal Detector

Animal detection system using YOLO for detecting rabbits, foxes, wild boars, birds, and other animals using GPU acceleration.

## Documentation

- **[Quick Start Training Guide](docs/QUICK_START_TRAINING.md)** - Get started training your model in 6 simple steps
- **[Complete Training Guide](docs/TRAINING_GUIDE.md)** - Comprehensive guide covering dataset preparation, annotation, and training
- **[Settings Guide](docs/SETTINGS_GUIDE.md)** - Detailed configuration management with `python-simple-settings`
- **[Models Guide](docs/MODELS_GUIDE.md)** - Understanding YOLO model types and choosing the right one
- **[Dataset Management](docs/DATASET_MANAGEMENT.md)** - Managing datasets with configurable names and templates
- **[Training FAQ](docs/TRAINING_FAQ.md)** - Common questions and troubleshooting tips
- **[Training Setup Summary](docs/TRAINING_SETUP_SUMMARY.md)** - Quick reference for training configuration

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

The project uses `python-simple-settings` for configuration management. Settings in `settings_local.py` override those in `settings.py`.

📖 **See [Settings Guide](docs/SETTINGS_GUIDE.md) for complete configuration details**

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

### YOLO Model Selection

📖 **See [Models Guide](docs/MODELS_GUIDE.md) for detailed model comparison**

Higher YOLO versions and larger model sizes generally perform better:

**Model Sizes:**
- **n (nano)**: Fastest, lowest accuracy (~6-10 MB)
- **s (small)**: Fast, good accuracy (~20-25 MB)
- **m (medium)**: Balanced speed and accuracy (~40-50 MB)
- **l (large)**: Slower, high accuracy (~80-100 MB)
- **x (extra-large)**: Slowest, highest accuracy (~130-150 MB)

**YOLO Versions:**
- **YOLOv8**: Mature, well-tested
- **YOLO11**: Latest, improved accuracy and speed

Set your preferred model in `settings.py`:
```python
MODEL_PATH = "yolo11l.pt"  # YOLO11 large for best accuracy
```

## Project Structure

```
AnimalDetector/
├── main.py                    # Main entry point
├── settings.py                # Default configuration
├── settings_local.py          # Local overrides (gitignored)
├── requirements.txt           # Python dependencies
├── results.csv                # Detection results (generated)
├── docs/                      # Documentation
│   ├── QUICK_START_TRAINING.md
│   ├── TRAINING_GUIDE.md
│   ├── SETTINGS_GUIDE.md
│   ├── MODELS_GUIDE.md
│   ├── DATASET_MANAGEMENT.md
│   ├── TRAINING_FAQ.md
│   └── TRAINING_SETUP_SUMMARY.md
├── datasets/                  # Training datasets
│   └── fototrampeo_bosque/   # Example dataset
├── gpu/                       # GPU detection utilities
│   └── gpu.py
├── logger/                    # Logging configuration
│   └── config.py
├── logs/                      # Application logs
│   └── animal_detector.log
├── tests/                     # Unit tests
│   ├── test_animal_detector.py
│   ├── test_detection.py
│   ├── test_training.py
│   └── ...
└── yolo/                      # YOLO detection and training
    ├── yolo.py                # Main detection logic
    ├── detection.py           # Detection classes
    ├── training.py            # Model training
    ├── model_registry.py      # Model management
    ├── create_dataset_structure.py
    ├── split_dataset.py
    ├── validate_dataset.py
    └── models/                # Downloaded YOLO models
```

## Training Custom Models

📖 **New to training? Start with [Quick Start Training Guide](docs/QUICK_START_TRAINING.md)**

📖 **For comprehensive training instructions, see [Complete Training Guide](docs/TRAINING_GUIDE.md)**

### Quick Training Example

```python
from yolo.training import ModelTrainer
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

### Dataset Management

The project includes tools for dataset creation and management:

```bash
# Create dataset structure
python -m yolo.create_dataset_structure --dataset my_animals

# Split images into train/val/test sets
python -m yolo.split_dataset --dataset my_animals

# Validate dataset format
python -m yolo.validate_dataset --dataset my_animals
```

📖 **See [Dataset Management](docs/DATASET_MANAGEMENT.md) for advanced dataset features**

### Training Resources

- **[Quick Start (6 steps)](docs/QUICK_START_TRAINING.md)** - Fast track to your first trained model
- **[Complete Guide](docs/TRAINING_GUIDE.md)** - In-depth training walkthrough
- **[Training FAQ](docs/TRAINING_FAQ.md)** - Troubleshooting and common questions
- **[Setup Summary](docs/TRAINING_SETUP_SUMMARY.md)** - Quick reference checklist


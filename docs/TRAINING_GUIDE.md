# YOLO Model Training Guide for Animal Detection

This comprehensive guide will walk you through the entire process of training a custom YOLO model to detect specific animals.

## Table of Contents
1. [Overview](#overview)
2. [Dataset Preparation](#dataset-preparation)
3. [Dataset Structure](#dataset-structure)
4. [Annotation Format](#annotation-format)
5. [Creating the Dataset Configuration](#creating-the-dataset-configuration)
6. [Training Process](#training-process)
7. [Evaluation and Testing](#evaluation-and-testing)
8. [Using Your Trained Model](#using-your-trained-model)
9. [Common Issues and Solutions](#common-issues-and-solutions)

---

## Overview

Training a YOLO model involves:
1. **Collecting images** of the animals you want to detect
2. **Annotating** those images (drawing boxes around animals)
3. **Organizing** the data in the correct format
4. **Configuring** the training parameters
5. **Training** the model
6. **Evaluating** the results
7. **Using** the trained model for detection

**Minimum Requirements:**
- At least 100-300 images per animal class (more is better)
- Images should represent different angles, lighting, backgrounds
- GPU recommended for faster training (NVIDIA with CUDA support)

---

## Dataset Preparation

### Step 1: Collect Images

Gather images containing the animals you want to detect:
- **Variety**: Different angles, distances, lighting conditions
- **Quality**: Good resolution (at least 640x640 recommended)
- **Quantity**: Minimum 100-300 images per class, 1000+ ideal
- **Format**: JPG or PNG

**Example animals from your project:**
- Rabbits
- Foxes
- Wild boars
- Birds

### Step 2: Annotate Your Images

You need to draw bounding boxes around each animal in your images. Use one of these tools:

#### Option A: LabelImg (Recommended for Beginners)
```bash
pip install labelImg
labelImg
```

**How to use:**
1. Open LabelImg
2. Click "Open Dir" and select your images folder
3. Click "Change Save Dir" and select where to save labels
4. Set format to "YOLO" (important!)
5. Draw boxes around animals: Press 'w' to create box
6. Label each box with the animal name
7. Press 'd' to go to next image
8. Repeat for all images

#### Option B: Roboflow (Cloud-based, easier)
1. Go to https://roboflow.com
2. Create a free account
3. Upload your images
4. Use their web interface to draw boxes
5. Export in "YOLO v8" format
6. Download the dataset

#### Option C: CVAT (Advanced, team collaboration)
```bash
# Install CVAT using Docker
docker-compose up -d
```
Visit: https://www.cvat.ai

### Step 3: Split Dataset

Split your annotated data into three sets:
- **Train (70-80%)**: Used to train the model
- **Validation (10-15%)**: Used during training to check progress
- **Test (10-15%)**: Used after training to evaluate final performance

---

## Dataset Structure

Your dataset must follow this exact structure:

```
datasets/
└── animal_dataset/
    ├── data.yaml              # Configuration file (required)
    ├── train/
    │   ├── images/
    │   │   ├── img001.jpg
    │   │   ├── img002.jpg
    │   │   └── ...
    │   └── labels/
    │       ├── img001.txt     # Same name as image
    │       ├── img002.txt
    │       └── ...
    ├── val/
    │   ├── images/
    │   │   ├── img101.jpg
    │   │   └── ...
    │   └── labels/
    │       ├── img101.txt
    │       └── ...
    └── test/
        ├── images/
        │   ├── img201.jpg
        │   └── ...
        └── labels/
            ├── img201.txt
            └── ...
```

**Important Rules:**
- Each image file must have a corresponding label file with the same name
- Image: `img001.jpg` → Label: `img001.txt`
- Label files are plain text, one line per object

---

## Annotation Format

Each label file (`.txt`) contains one line per detected object in the image.

**Format per line:**
```
<class_id> <x_center> <y_center> <width> <height>
```

**Values:**
- `class_id`: Integer starting from 0 (0=rabbit, 1=fox, 2=wild_boar, 3=bird)
- `x_center`: Center X coordinate (0.0 to 1.0, normalized by image width)
- `y_center`: Center Y coordinate (0.0 to 1.0, normalized by image height)
- `width`: Box width (0.0 to 1.0, normalized by image width)
- `height`: Box height (0.0 to 1.0, normalized by image height)

**Example label file (img001.txt):**
```
0 0.516 0.623 0.143 0.267
1 0.234 0.456 0.089 0.156
```

This means:
- Line 1: A rabbit (class 0) at center (51.6%, 62.3%) with size (14.3%, 26.7%)
- Line 2: A fox (class 1) at center (23.4%, 45.6%) with size (8.9%, 15.6%)

**Coordinate Calculation:**
If your image is 1920x1080 pixels and a rabbit box is:
- Top-left: (800, 400)
- Bottom-right: (1100, 700)

Calculate:
```
x_center = ((800 + 1100) / 2) / 1920 = 0.494
y_center = ((400 + 700) / 2) / 1080 = 0.509
width = (1100 - 800) / 1920 = 0.156
height = (700 - 400) / 1080 = 0.278
```

Result: `0 0.494 0.509 0.156 0.278`

---

## Creating the Dataset Configuration

Create a `data.yaml` file in your dataset root directory.

**File: `datasets/animal_dataset/data.yaml`**
```yaml
# Path to dataset root (absolute or relative to this file)
path: /home/rafa/PycharmProjects/AnimalDetector/datasets/animal_dataset

# Paths to train/val/test splits (relative to 'path')
train: train/images
val: val/images
test: test/images

# Number of classes
nc: 4

# Class names (must match the order of class_id in labels)
names:
  0: rabbit
  1: fox
  2: wild_boar
  3: bird
```

**Important:**
- Use absolute paths or paths relative to the YAML file
- Class names must be in order matching your class IDs
- `nc` must equal the number of classes

---

## Training Process

### Method 1: Using the Training Script (Recommended)

Create and run the training script:

```bash
python train_model.py
```

The script handles all training configuration and saves results automatically.

### Method 2: Manual Training (Advanced)

```python
from pathlib import Path
from yolo.training import ModelTrainer

# Configuration
model_path = Path("yolo/models/yolo11n.pt")  # Base model
data_config = Path("datasets/animal_dataset/data.yaml")
device = "0"  # Use GPU 0, or "cpu" for CPU

# Training parameters
epochs = 100  # Number of training iterations
image_size = 640  # Input image size
batch_size = 16  # Images per batch (reduce if GPU memory error)

# Create trainer
trainer = ModelTrainer(model_path, device)

# Start training
results = trainer.train(
    data_config=data_config,
    epochs=epochs,
    image_size=image_size,
    batch_size=batch_size
)

# Save trained model
output_path = Path("yolo/models/custom_animal_detector.pt")
trainer.save_model(output_path)
```

### Training Parameters Explained

**epochs (default: 100)**
- Number of times the model sees all training images
- More epochs = better learning (but risk overfitting)
- Start with 50-100, increase if validation loss still decreasing

**image_size (default: 640)**
- Images resized to this dimension (640x640, 1280x1280, etc.)
- Larger = better accuracy but slower training
- Use 640 for fast training, 1280 for best accuracy

**batch_size (default: 16)**
- Number of images processed simultaneously
- Larger = faster training but needs more GPU memory
- Reduce if you get "CUDA out of memory" errors
- Typical values: 8, 16, 32

**device**
- "0": Use first GPU
- "cpu": Use CPU (much slower)
- "0,1": Use multiple GPUs

### Choosing a Base Model

Start with a pre-trained YOLO model:

| Model | Speed | Accuracy | Best For |
|-------|-------|----------|----------|
| yolo11n.pt | Fastest | Good | Real-time detection, embedded devices |
| yolo11s.pt | Fast | Better | Balanced performance |
| yolo11m.pt | Medium | Very Good | Good balance |
| yolo11l.pt | Slow | Excellent | Best accuracy needed |
| yolo11x.pt | Slowest | Best | Maximum accuracy |

**Recommendation:** Start with `yolo11n.pt` for quick experiments, use `yolo11m.pt` or `yolo11l.pt` for production.

### Expected Training Output

```
Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
  1/100      3.5G      1.234      2.456      1.123        150        640
  2/100      3.5G      1.123      2.234      1.034        148        640
  ...
 50/100      3.5G      0.234      0.456      0.234        145        640
 ...
100/100      3.5G      0.123      0.234      0.123        142        640

Training complete. Results saved to runs/detect/train/
```

**What to monitor:**
- **box_loss**: How accurate the bounding boxes are (should decrease)
- **cls_loss**: How accurate the classifications are (should decrease)
- **GPU_mem**: GPU memory usage
- All losses should trend downward

---

## Evaluation and Testing

### Evaluate Model Performance

```python
from pathlib import Path
from yolo.training import ModelTrainer

# Load your trained model
model_path = Path("runs/detect/train/weights/best.pt")
trainer = ModelTrainer(model_path, device="0")

# Evaluate on test set
data_config = Path("datasets/animal_dataset/data.yaml")
results = trainer.evaluate(data_config)

print(f"mAP50: {results.box.map50}")
print(f"mAP50-95: {results.box.map}")
```

### Understanding Metrics

**mAP (mean Average Precision):**
- mAP50: Average precision at 50% IoU threshold
- mAP50-95: Average across multiple IoU thresholds (50% to 95%)
- Higher is better (0.0 to 1.0)

**Good Performance:**
- mAP50 > 0.7: Good
- mAP50 > 0.8: Very good
- mAP50 > 0.9: Excellent

**Per-Class Metrics:**
- Precision: Of all detected rabbits, how many were actually rabbits?
- Recall: Of all actual rabbits, how many did we detect?

### Visualize Results

After training, results are saved to `runs/detect/train/`:
- `weights/best.pt`: Best model during training
- `weights/last.pt`: Model from last epoch
- `confusion_matrix.png`: Shows classification errors
- `results.png`: Training curves (losses, metrics over time)
- `val_batch0_pred.jpg`: Example predictions on validation set

**Review these files to understand model performance!**

---

## Using Your Trained Model

### Update Settings

Edit `settings.py` or `settings_local.py`:

```python
# Use your trained model
MODEL_PATH = Path('runs/detect/train/weights/best.pt')

# Update target animals if needed
TARGET_ANIMALS = ["rabbit", "fox", "wild_boar", "bird"]
```

### Run Detection

```bash
python main.py
```

The detector will now use your custom trained model!

### Test Single Image

```python
from pathlib import Path
from yolo.detection import AnimalDetector

# Load your trained model
model_path = Path("runs/detect/train/weights/best.pt")
detector = AnimalDetector(
    model_path=model_path,
    device="0",
    confidence_threshold=0.25
)

# Detect animals
image_path = Path("test_image.jpg")
detections = detector.detect_animals_in_image(
    image_path,
    target_animals=["rabbit", "fox", "wild_boar", "bird"]
)

for detection in detections:
    print(f"Found {detection['class_name']} with confidence {detection['confidence']:.2f}")
```

---

## Common Issues and Solutions

### Issue: "CUDA out of memory"
**Solution:** Reduce batch size
```python
# Try smaller batch sizes
batch_size = 8  # or 4, or even 1
```

### Issue: "No labels found"
**Solution:** Check dataset structure
- Ensure labels folder exists alongside images folder
- Verify label files have same names as images (except extension)
- Check data.yaml paths are correct

### Issue: Training loss not decreasing
**Solutions:**
- Increase learning rate: Add `lr0=0.01` to training args
- Train longer: Increase epochs
- Check annotations: Verify labels are correct
- More data: Collect more images

### Issue: Good training metrics but poor real-world performance
**Solutions:**
- More diverse training data needed
- Add data augmentation (YOLO does this automatically)
- Collect images similar to your real-world scenario

### Issue: Model detects animals but wrong species
**Solutions:**
- Check class_id mapping in data.yaml
- Ensure label files use correct class IDs
- Add more training examples of confused species

### Issue: Training very slow
**Solutions:**
- Use smaller model (yolo11n instead of yolo11l)
- Reduce image_size (640 instead of 1280)
- Ensure GPU is being used (check DEVICE setting)
- Use fewer epochs for initial testing

---

## Quick Start Checklist

- [ ] Install required packages: `pip install ultralytics labelImg`
- [ ] Collect at least 100-300 images per animal class
- [ ] Annotate images using LabelImg or Roboflow
- [ ] Organize into train/val/test splits (70/15/15)
- [ ] Create data.yaml configuration file
- [ ] Verify dataset structure matches required format
- [ ] Download base model: `python download_models.py`
- [ ] Create and run training script
- [ ] Monitor training progress (losses decreasing)
- [ ] Evaluate model on test set
- [ ] Update settings.py with trained model path
- [ ] Test on new images

---

## Additional Resources

**Official YOLO Documentation:**
- https://docs.ultralytics.com/modes/train/

**Dataset Tools:**
- LabelImg: https://github.com/tzutalin/labelImg
- Roboflow: https://roboflow.com
- CVAT: https://www.cvat.ai

**Pre-annotated Datasets:**
- Roboflow Universe: https://universe.roboflow.com
- Open Images: https://storage.googleapis.com/openimages/web/index.html

**Tips:**
- Start small: Test with 50 images first
- Use GPU: Training on CPU can take days
- Monitor progress: Check validation metrics
- Iterate: Train → Evaluate → Improve → Repeat

---

## Support

If you encounter issues:
1. Check the logs in `logs/animal_detector.log`
2. Review the training output in `runs/detect/train/`
3. Verify your dataset structure matches the guide
4. Ensure all paths in data.yaml are correct
5. Test with a smaller dataset first


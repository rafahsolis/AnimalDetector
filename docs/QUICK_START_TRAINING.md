# Quick Start: Train Your Animal Detection Model

This is a condensed guide to get you training as quickly as possible.

## Prerequisites

**System Dependencies (Linux only):**
```bash
sudo apt-get update
sudo apt-get install -y libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0
```

**Python Dependencies:**
```bash
pip install ultralytics labelImg
```

## 6-Step Process (Simplified!)

### Step 1: Create Dataset Structure (30 seconds)
```bash
python -m yolo.create_dataset_structure --dataset animal_dataset
```

This automatically creates:
- `datasets/animal_dataset/images/` (for your images)
- `datasets/animal_dataset/labels/` (for annotations)
- `datasets/animal_dataset/README.md` (instructions)

Now put all your images in `datasets/animal_dataset/images/`

### Step 2: Annotate Images (Most Time-Consuming)

**Option A: LabelImg (Desktop)**
```bash
labelImg datasets/animal_dataset/images datasets/animal_dataset/labels
```
1. Click "PascalVOC" button → Change to "YOLO"
2. Press 'W' → Draw box around animal
3. Type animal name (rabbit, fox, wild_boar, bird)
4. Press 'D' → Next image
5. Repeat for all images

Labels will be saved to `datasets/animal_dataset/labels/`

**Option B: Roboflow (Web-based, Easier)**
1. Go to https://roboflow.com
2. Create free account
3. Upload images
4. Draw boxes in browser
5. Export as "YOLOv8"
6. Download and extract to dataset folder

### Step 3: Split Dataset (30 seconds)
```bash
python -m yolo.split_dataset
```

This automatically splits your annotated images into:
- 70% training
- 15% validation
- 15% testing

**Custom split ratios?** Edit `yolo/split_dataset.py`:
```python
def create_default_ratios() -> SplitRatios:
    return SplitRatios(train=0.8, val=0.1, test=0.1)  # 80/10/10
```

**Different random seed?** Change in `main()`:
```python
splitter = DatasetSplitter(paths, ratios, random_seed=123)
```

### Step 4: Configure Dataset (2 minutes)
```bash
# Copy example config
cp datasets/animal_dataset/data.yaml.example datasets/animal_dataset/data.yaml
# Edit with your editor
nano datasets/animal_dataset/data.yaml
```

Update the `path` line to your absolute path:
```yaml
path: /home/rafa/PycharmProjects/AnimalDetector/datasets/animal_dataset
```

### Step 5: Download Base Model (1 minute)
```bash
python -m yolo.download_models
```

### Step 6: Train! (Hours to Days)
```bash
python -m yolo.train_model
```

**Training Options:**
Edit the `create_training_parameters()` function in `yolo/train_model.py`:
```python
# In yolo/train_model.py, find and modify this function:

def create_training_parameters() -> TrainingParameters:
    epochs = 50        # Try 50 first, then increase to 100+
    image_size = 640   # Use 640 for speed, 1280 for accuracy
    batch_size = 16    # Reduce to 8 or 4 if GPU memory error
    
    return TrainingParameters(epochs, image_size, batch_size)
```

**GPU Memory Issues?**
```python
batch_size = 4  # Reduce this value
```

## Monitor Progress

Watch the training output:
```
Epoch    GPU_mem   box_loss   cls_loss   dfl_loss
  1/50      3.5G      1.234      2.456      1.123  ← Should decrease
 25/50      3.5G      0.456      0.789      0.456  ← Getting better
 50/50      3.5G      0.234      0.345      0.234  ← Good!
```

## Check Results

After training:
```bash
ls runs/detect/train/weights/
# best.pt  ← Use this one!
# last.pt  ← Or this if best.pt doesn't exist

# View training curves and predictions
xdg-open runs/detect/train/results.png
xdg-open runs/detect/train/val_batch0_pred.jpg
```

## Use Your Model

Update `settings_local.py`:
```python
from pathlib import Path
MODEL_PATH = Path('runs/detect/train/weights/best.pt')
```

Run detection:
```bash
python main.py
```

## Minimum Requirements

| Item | Minimum | Recommended |
|------|---------|-------------|
| Images per class | 100 | 500+ |
| Image resolution | 640x640 | 1920x1080 |
| GPU VRAM | 4GB | 8GB+ |
| Training time | 2-4 hours | Varies |

## Common Issues

**"Could not load Qt platform plugin xcb" (labelImg error on Linux)**
→ Install system dependencies:
```bash
sudo apt-get install -y libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0
```

**"CUDA out of memory"**
→ Reduce batch_size to 4 or 8

**"No labels found"**
→ Check labels are in correct folders with same names as images

**"Training loss not decreasing"**
→ Train longer (more epochs) or check your annotations

**"Model not detecting animals"**
→ Need more training data or train for more epochs

## Next Steps

1. ✓ Train model
2. Evaluate: Check `runs/detect/train/results.png`
3. Test: Run on new images with `python main.py`
4. Improve: Add more data and retrain if needed

## Need More Help?

Read the comprehensive guide:
```bash
cat docs/TRAINING_GUIDE.md
```


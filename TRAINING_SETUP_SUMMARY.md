# Training Setup - Summary

## ✅ What Has Been Created

I've set up everything you need to train your custom animal detection model:

### 📁 Dataset Structure
```
datasets/animal_dataset/
├── README.md                      # Dataset instructions
├── data.yaml.example              # Configuration template
├── label_format_example.txt       # Label format reference
├── train/
│   ├── images/                   # Put 70% of your images here
│   └── labels/                   # Put 70% of your labels here
├── val/
│   ├── images/                   # Put 15% of your images here
│   └── labels/                   # Put 15% of your labels here
└── test/
    ├── images/                   # Put 15% of your images here
    └── labels/                   # Put 15% of your labels here
```

### 📄 Documentation Files
1. **docs/TRAINING_GUIDE.md** - Comprehensive 200+ line guide covering:
   - Complete dataset preparation
   - Annotation tools and techniques
   - Training process explained
   - Parameter tuning
   - Evaluation and metrics
   - Common issues and solutions

2. **docs/QUICK_START_TRAINING.md** - 5-step quick start guide for fast setup

3. **docs/TRAINING_FAQ.md** - 50+ frequently asked questions with answers

### 🔧 Helper Scripts
1. **create_dataset_structure.py** - Creates the dataset folder structure
2. **train_model.py** - Ready-to-use training script
3. **validate_dataset.py** - Validates your dataset before training

### 📦 Updated Files
- **requirements.txt** - Added `labelImg` and `PyYAML`
- **README.md** - Updated with training section

---

## 🚀 Quick Start (5 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Collect and Annotate Images
**Option A: LabelImg (Desktop Tool)**
```bash
labelImg
```
1. Click "Open Dir" → Select your images folder
2. Click "Change Save Dir" → Select the labels folder
3. Click "PascalVOC" → Change to "YOLO" format
4. Press 'W' to draw box around animal
5. Type animal name (rabbit, fox, wild_boar, bird)
6. Press 'D' for next image
7. Repeat for all images

**Option B: Roboflow (Web-based, Easier)**
1. Go to https://roboflow.com (free account)
2. Upload your images
3. Draw boxes in your browser
4. Export as "YOLOv8" format
5. Download and place in dataset folders

**Minimum Requirements:**
- 100-300 images per animal type
- Mix of angles, lighting, backgrounds
- Good resolution (640x640 minimum)

### Step 3: Organize Your Dataset
```bash
# Place your images and labels:
# 70% in datasets/animal_dataset/train/images/ and train/labels/
# 15% in datasets/animal_dataset/val/images/ and val/labels/
# 15% in datasets/animal_dataset/test/images/ and test/labels/

# Each image needs a matching label file:
# rabbit001.jpg → rabbit001.txt
# fox042.jpg → fox042.txt
```

### Step 4: Configure Dataset
```bash
# Copy the example config
cp datasets/animal_dataset/data.yaml.example datasets/animal_dataset/data.yaml

# Edit the file
nano datasets/animal_dataset/data.yaml

# Update the 'path' line with your absolute path:
path: /home/rafa/PycharmProjects/AnimalDetector/datasets/animal_dataset
```

### Step 5: Validate and Train
```bash
# Validate your dataset
python validate_dataset.py

# If validation passes, start training!
python train_model.py
```

---

## 📊 Training Configuration

The `train_model.py` script is pre-configured with sensible defaults:

```python
# Base model: yolo11n.pt (fast, good for testing)
# Epochs: 100 (how many times to see all images)
# Image size: 640 (input resolution)
# Batch size: 16 (images processed together)
# Device: "0" (GPU 0, change to "cpu" if no GPU)
```

**To customize**, edit the functions in `train_model.py`:
- `create_training_configuration()` - Change model, dataset path, device
- `create_training_parameters()` - Change epochs, image_size, batch_size

---

## ⏱️ Training Time Estimates

| Hardware | Dataset Size | Estimated Time |
|----------|--------------|----------------|
| RTX 4090 | 1000 images | 1-2 hours |
| RTX 3060 | 1000 images | 2-4 hours |
| GTX 1080 | 1000 images | 4-6 hours |
| CPU only | 1000 images | 1-3 days ⚠️ |

---

## 📈 After Training

Results will be saved to `runs/detect/train/`:

```bash
runs/detect/train/
├── weights/
│   ├── best.pt          # ← Your trained model (use this!)
│   └── last.pt          # Last epoch model
├── results.png          # Training metrics visualization
├── confusion_matrix.png # Classification accuracy
└── val_batch0_pred.jpg  # Example predictions
```

**To use your trained model:**
1. Open `settings_local.py` (create if doesn't exist)
2. Add: `MODEL_PATH = Path('runs/detect/train/weights/best.pt')`
3. Run: `python main.py`

---

## 📚 Need More Help?

### Read the Guides
```bash
# Comprehensive guide (everything you need to know)
cat docs/TRAINING_GUIDE.md

# Quick start (condensed version)
cat docs/QUICK_START_TRAINING.md

# FAQ (common questions answered)
cat docs/TRAINING_FAQ.md
```

### Common Issues

**"CUDA out of memory"**
→ Edit `train_model.py`, reduce `batch_size = 8` or `batch_size = 4`

**"No labels found"**
→ Run `python validate_dataset.py` to check your dataset

**Training is very slow**
→ Ensure GPU is enabled, check `DEVICE = "0"` in script

**Model not detecting animals**
→ Need more training data or more epochs

---

## 📝 Label Format Reference

Each label file contains one line per animal in the image:
```
<class_id> <x_center> <y_center> <width> <height>
```

**Example:**
```
0 0.516 0.623 0.143 0.267
```
- Class 0 (rabbit)
- Center at (51.6%, 62.3%) of image
- Size (14.3%, 26.7%) of image

**Class IDs:**
- 0 = rabbit
- 1 = fox
- 2 = wild_boar
- 3 = bird

---

## ✨ Tips for Best Results

1. **Start Small**: Test with 50 images first to validate workflow
2. **Quality > Quantity**: 500 good images > 2000 poor images
3. **Variety**: Different angles, lighting, distances, backgrounds
4. **Consistency**: Annotate similarly across all images
5. **Validation**: Always run `validate_dataset.py` before training
6. **Monitor**: Watch the training output, check if losses decrease
7. **Evaluate**: Review `results.png` and `confusion_matrix.png`
8. **Iterate**: Train → Evaluate → Add more data → Retrain

---

## 🎯 Your Next Actions

1. [ ] Install labelImg: `pip install labelImg`
2. [ ] Collect images of your target animals
3. [ ] Annotate images using labelImg or Roboflow
4. [ ] Organize images into train/val/test folders
5. [ ] Copy and edit `data.yaml`
6. [ ] Run validation: `python validate_dataset.py`
7. [ ] Start training: `python train_model.py`
8. [ ] Check results in `runs/detect/train/`
9. [ ] Update settings to use your trained model
10. [ ] Test on new images!

---

## 📞 Quick Command Reference

```bash
# Setup
python create_dataset_structure.py

# Annotation
labelImg

# Validation
python validate_dataset.py

# Training
python train_model.py

# Detection with trained model
python main.py

# View results
ls -la runs/detect/train/
xdg-open runs/detect/train/results.png
```

---

Good luck with your training! 🚀


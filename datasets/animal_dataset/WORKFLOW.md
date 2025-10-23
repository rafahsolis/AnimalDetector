# Simplified Dataset Workflow

This guide explains the new simplified approach to creating your training dataset.

## Quick Start

### 1. Put all images in one folder
```bash
mkdir -p datasets/animal_dataset/images
# Copy all your images here
```

### 2. Annotate with labelImg
```bash
labelImg datasets/animal_dataset/images datasets/animal_dataset/labels
```
- Change to YOLO format (click "PascalVOC" button)
- Draw boxes around animals
- Labels are saved automatically to `labels/` folder

### 3. Split into train/val/test
```bash
python -m yolo.split_dataset
```
This automatically:
- Copies 70% of images to `train/`
- Copies 15% of images to `val/`
- Copies 15% of images to `test/`
- Copies corresponding labels too
- Keeps originals in `images/` and `labels/`

## Customization

### Change Split Ratios

Edit `yolo/split_dataset.py`:

```python
def create_default_ratios() -> SplitRatios:
    return SplitRatios(train=0.8, val=0.1, test=0.1)
```

### Change Random Seed

Edit the `main()` function in `yolo/split_dataset.py`:

```python
splitter = DatasetSplitter(paths, ratios, random_seed=123)
```

Using the same seed ensures you get the same split every time (reproducible).

## Folder Structure

**Before splitting:**
```
datasets/animal_dataset/
├── images/           # All your images here
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
└── labels/           # All corresponding labels here
    ├── img1.txt
    ├── img2.txt
    └── ...
```

**After splitting:**
```
datasets/animal_dataset/
├── images/           # Original images (preserved)
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
├── labels/           # Original labels (preserved)
│   ├── img1.txt
│   ├── img2.txt
│   └── ...
├── train/
│   ├── images/       # 70% of images (copied)
│   └── labels/       # 70% of labels (copied)
├── val/
│   ├── images/       # 15% of images (copied)
│   └── labels/       # 15% of labels (copied)
└── test/
    ├── images/       # 15% of images (copied)
    └── labels/       # 15% of labels (copied)
```

## Important Notes

✅ **The split operation COPIES files** (doesn't move). Your original `images/` and `labels/` folders are preserved.

⚠️ **Existing split folders are cleared** before splitting to avoid duplicates.

💡 **Uses more disk space** since files are copied rather than moved. Make sure you have sufficient space.

## Next Steps

After splitting:
1. Configure `data.yaml`
2. Download base models: `python -m yolo.download_models`
3. Train: `python -m yolo.train_model`


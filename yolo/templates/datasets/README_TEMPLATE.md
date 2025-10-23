# Animal Detection Dataset - Simplified Workflow

## Quick Start

This dataset uses a simplified workflow:

1. Put all images in `images/` folder
2. Annotate them (labels go to `labels/` folder)
3. Run the split script to create train/val/test splits

## Structure

**Initial structure (for annotation):**
```
animal_dataset/
├── images/              # Put ALL your images here
└── labels/              # Annotations go here (YOLO format)
```

**After running split script:**
```
animal_dataset/
├── images/              # Original images (preserved)
├── labels/              # Original labels (preserved)
├── data.yaml            # Configuration file
├── train/
│   ├── images/          # 70% of images (copied)
│   └── labels/          # 70% of labels (copied)
├── val/
│   ├── images/          # 15% of images (copied)
│   └── labels/          # 15% of labels (copied)
└── test/
    ├── images/          # 15% of images (copied)
    └── labels/          # 15% of labels (copied)
```

## Next Steps

1. **Add images**: Copy all your images to `images/` folder
2. **Annotate**: Use labelImg or Roboflow to create labels
   ```bash
   labelImg images/ labels/
   ```
3. **Split dataset**: Run the automated split script
   ```bash
   python -m yolo.split_dataset
   ```
4. **Configure**: Copy and edit data.yaml
   ```bash
   cp data.yaml.example data.yaml
   nano data.yaml  # Update paths
   ```
5. **Download models**: Get pre-trained weights
   ```bash
   python -m yolo.download_models
   ```
6. **Train**: Start training your model
   ```bash
   python -m yolo.train_model
   ```

## Label Format

Each label file is a text file with one line per object:
```
<class_id> <x_center> <y_center> <width> <height>
```

Example (rabbit in center of image):
```
0 0.5 0.5 0.2 0.3
```

All values are normalized (0.0 to 1.0).

## Annotation Tools

- **LabelImg** (recommended): Desktop app
  ```bash
  pip install labelImg
  labelImg images/ labels/
  ```
  Remember to select YOLO format!

- **Roboflow**: Web-based, easier for beginners
  - https://roboflow.com
  - Export as "YOLOv8 format"

- **CVAT**: Advanced, team collaboration
  - https://www.cvat.ai

## Need Help?

See `WORKFLOW.md` for detailed instructions.


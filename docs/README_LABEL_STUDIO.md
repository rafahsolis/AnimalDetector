# Label Studio Integration - Complete Package

## 📦 What's Included

This package provides complete Label Studio integration for annotating camera trap images for YOLOv11 training.

### ✅ Features

- **Label Studio configuration** optimized for camera trap annotation
- **Automated conversion** from Label Studio JSON to YOLO format
- **Duplicate detection** using SHA256 hashing
- **Dataset validation** with comprehensive statistics
- **Auto-generation** of training configs
- **Dataset initialization** tools
- **Complete documentation** with examples
- **Unit tests** for all core functionality

## 📚 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [LABEL_STUDIO_GUIDE.md](LABEL_STUDIO_GUIDE.md) | Complete annotation workflow guide | All users |
| [LABEL_STUDIO_QUICK_REF.md](LABEL_STUDIO_QUICK_REF.md) | Command reference | Power users |
| [DATASET_MIGRATION.md](DATASET_MIGRATION.md) | Migrate existing datasets | Current users |
| [LABEL_STUDIO_IMPLEMENTATION.md](LABEL_STUDIO_IMPLEMENTATION.md) | Technical details | Developers |

## 🚀 Quick Start

### For New Datasets

```bash
# 1. Initialize
python -m yolo.init_dataset my_camera_trap_dataset

# 2. Add images
cp /source/images/*.jpg datasets/my_camera_trap_dataset/images/

# 3. Start Label Studio
docker run -it -p 8080:8080 -v $(pwd)/label-studio-data:/label-studio/data \
    heartexlabs/label-studio:latest

# 4. Annotate in browser (http://localhost:8080)

# 5. Export and convert
python -m yolo.label_studio_to_yolo \
    --json export.json \
    --images datasets/my_camera_trap_dataset/images \
    --labels datasets/my_camera_trap_dataset/labels \
    --classes datasets/my_camera_trap_dataset/labels/classes.txt

# 6. Validate
python -m yolo.validate_annotations \
    --images datasets/my_camera_trap_dataset/images \
    --labels datasets/my_camera_trap_dataset/labels \
    --classes datasets/my_camera_trap_dataset/labels/classes.txt

# 7. Split and train
python -m yolo.split_dataset --dataset my_camera_trap_dataset
python -m yolo.generate_data_yaml --dataset my_camera_trap_dataset
python -m yolo.train_model
```

### For Existing Dataset (fototrampeo_bosque)

See [DATASET_MIGRATION.md](DATASET_MIGRATION.md) for migration instructions.

## 📁 File Structure

```
yolo/
├── label_studio_config.xml          # Label Studio UI configuration
├── label_studio_to_yolo.py          # Converter: JSON → YOLO format
├── validate_annotations.py          # Dataset quality analysis
├── generate_data_yaml.py            # Auto-generate training config
├── init_dataset.py                  # Initialize new datasets
└── split_dataset.py                 # Split train/val/test (updated)

docs/
├── LABEL_STUDIO_GUIDE.md            # Complete guide (500+ lines)
├── LABEL_STUDIO_QUICK_REF.md        # Quick reference
├── DATASET_MIGRATION.md             # Migration guide
├── LABEL_STUDIO_IMPLEMENTATION.md   # Technical documentation
└── README_LABEL_STUDIO.md           # This file

tests/
└── test_label_studio_conversion.py  # Unit tests (10 tests)
```

## 🎯 Use Cases

### 1. **Manual Annotation from Scratch**

Best for: New datasets, high-quality annotations

```bash
python -m yolo.init_dataset wildlife_camera_1
# Add images, annotate in Label Studio, convert
```

### 2. **Incremental Annotation**

Best for: Growing datasets, new camera deployments

```bash
# Annotate new batch in Label Studio
# Export only new annotations
python -m yolo.label_studio_to_yolo --json new_batch.json ...
# Existing annotations are preserved
```

### 3. **Multi-Annotator Workflow**

Best for: Teams, quality control

- Set up Label Studio with multiple users
- Enable review mode
- Track inter-annotator agreement
- See [Multi-User Workflow](LABEL_STUDIO_GUIDE.md#multi-user-workflow)

### 4. **Pre-labeling + Review**

Best for: Large datasets, existing model

- Run detection with current model
- Import predictions to Label Studio
- Annotators review and correct
- (Requires custom import script - future enhancement)

## 🛠️ Tools Reference

### `label_studio_to_yolo.py`

**Purpose:** Convert Label Studio JSON export to YOLO format

**Key Features:**
- Automatic duplicate detection
- Flexible image path resolution
- Creates empty labels for negatives
- Validates bounding boxes

**Usage:**
```bash
python -m yolo.label_studio_to_yolo \
    --json export.json \
    --images datasets/DATASET/images \
    --labels datasets/DATASET/labels \
    --classes datasets/DATASET/labels/classes.txt \
    [--skip-duplicates]
```

### `validate_annotations.py`

**Purpose:** Analyze dataset quality

**Reports:**
- Image and annotation counts
- Class distribution
- Box size distribution
- Invalid/duplicate boxes
- Missing classes

**Usage:**
```bash
python -m yolo.validate_annotations \
    --images datasets/DATASET/images \
    --labels datasets/DATASET/labels \
    --classes datasets/DATASET/labels/classes.txt \
    [--output report.txt]
```

### `generate_data_yaml.py`

**Purpose:** Create YOLOv11 training config

**Output:** `data.yaml` with paths and class names

**Usage:**
```bash
python -m yolo.generate_data_yaml --dataset DATASET_NAME
```

### `init_dataset.py`

**Purpose:** Initialize new dataset structure

**Creates:**
- Directory structure
- classes.txt (default or custom)
- README.md

**Usage:**
```bash
# With default classes
python -m yolo.init_dataset my_dataset

# With custom classes
python -m yolo.init_dataset my_dataset --classes "dog,cat,bird"
```

## 🏗️ Dataset Structure

### Standardized Layout

```
datasets/<dataset_name>/
├── images/              # Original images
├── labels/              # YOLO annotations
│   └── classes.txt      # Class names
├── train/               # Training split
│   ├── images/
│   └── labels/
├── val/                 # Validation split
│   ├── images/
│   └── labels/
├── test/                # Test split
│   ├── images/
│   └── labels/
├── data.yaml            # YOLOv11 config
└── README.md            # Dataset docs
```

## 📊 Supported Annotations

### Bounding Boxes

8 default classes:
- `bird`
- `wild_boar`
- `rabbit`
- `roe_deer`
- `fox`
- `human` (distractor)
- `vehicle` (distractor)
- `unknown_animal`

### Metadata (Optional)

- **Gender:** male, female, unknown
- **Age class:** juvenile, adult, unknown
- **Time of day:** day, night, dawn/dusk
- **Behavior:** foraging, moving, resting, alert, grooming, interacting
- **Visibility:** clear, partially occluded, heavily occluded, motion blur
- **Notes:** Free text

> **Note:** Current implementation exports only bounding boxes. Metadata export is a future enhancement.

## 🧪 Testing

All core functionality is tested:

```bash
python -m unittest tests.test_label_studio_conversion -v
```

**Test Coverage:**
- Bounding box conversion accuracy
- Coordinate validation
- Class mapping
- Annotation extraction
- End-to-end conversion

**Result:** ✓ 10/10 tests passing

## 💡 Best Practices

### Annotation Quality

1. **Consistency:** Use same rules for all images
2. **Documentation:** Keep guidelines updated
3. **Quality checks:** Review 10% of annotations regularly
4. **Multiple annotators:** 2-3 annotators for critical datasets

### Dataset Management

1. **Version control:** Commit after each annotation batch
2. **Backups:** Daily export from Label Studio
3. **Validation:** Run validation before training
4. **Metadata:** Track camera location, date range, conditions

### Workflow

1. **Batch annotation:** Annotate 200-500 images at a time
2. **Incremental updates:** Add new images without re-annotating
3. **Split early:** Test train/val/test split before full annotation
4. **Monitor balance:** Check class distribution regularly

## 🐛 Troubleshooting

### Common Issues

**Images not found after export**
- Check filename case (`.JPG` vs `.jpg`)
- Use absolute paths
- Verify images are in `images/` directory

**Invalid bounding boxes**
- Boxes must be within image bounds
- Run validation to identify issues
- Re-annotate problematic images

**Class mismatch**
- Ensure class names in Label Studio match `classes.txt` exactly
- Class order doesn't matter, spelling does

**Label Studio won't start**
- Check if port 8080 is in use
- Try different port: `-p 8081:8080`
- Check Docker logs: `docker logs label-studio`

See [LABEL_STUDIO_GUIDE.md#troubleshooting](LABEL_STUDIO_GUIDE.md#troubleshooting) for more.

## 📈 Future Enhancements

Potential additions:

1. **Pre-labeling script:** Generate predictions from existing model
2. **Reverse converter:** YOLO → Label Studio (for editing)
3. **Metadata exporter:** Save attributes to separate files
4. **Multi-dataset merger:** Combine annotations from multiple projects
5. **Active learning:** Suggest most informative images
6. **Web dashboard:** Visualize statistics

## 🤝 Support

For help:

1. Check [LABEL_STUDIO_GUIDE.md](LABEL_STUDIO_GUIDE.md)
2. Read [TRAINING_FAQ.md](TRAINING_FAQ.md)
3. Review [Label Studio docs](https://labelstud.io/guide/)
4. Check existing issues

## 📝 License

Same as AnimalDetector project.

## 🎓 Learn More

- [Label Studio Documentation](https://labelstud.io/)
- [YOLOv11 Documentation](https://docs.ultralytics.com/)
- [YOLO Format Specification](https://docs.ultralytics.com/datasets/detect/)
- [Camera Trap ML Best Practices](https://github.com/agentmorris/MegaDetector)

---

**Created:** 2025-11-03  
**Version:** 1.0  
**Status:** Production Ready ✓


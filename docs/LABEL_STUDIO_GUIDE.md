# Label Studio Integration for YOLOv11 Training

This guide explains how to use Label Studio to annotate images for YOLOv11 training in the AnimalDetector project.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Setup Label Studio](#setup-label-studio)
3. [Create Annotation Project](#create-annotation-project)
4. [Annotate Images](#annotate-images)
5. [Export and Convert](#export-and-convert)
6. [Validate Dataset](#validate-dataset)
7. [Split Dataset](#split-dataset)
8. [Train Model](#train-model)
9. [Advanced Features](#advanced-features)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

**Complete workflow in 3 steps:**

```bash
# 1. Start Label Studio (easiest way)
cd label_studio
docker compose up -d

# Open http://localhost:8080 and annotate

# 2. Export from Label Studio and convert to YOLO
python -m label_studio.converter \
    --json export.json \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt

# 3. Validate, split, and train
python -m label_studio.validator \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt

python -m yolo.split_dataset --dataset fototrampeo_bosque
python -m yolo.generate_data_yaml --dataset fototrampeo_bosque
python -m yolo.train_model
```

**See `label_studio/README.md` for detailed setup instructions.**

---

## Setup Label Studio

### Option 1: Docker Compose (Recommended - Simplest!)

This is the easiest way - datasets are automatically mounted!

```bash
# Navigate to label_studio folder
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio

# Start Label Studio (first time and subsequent runs)
docker compose up -d

# View logs (optional)
docker compose logs -f

# Stop when done
docker compose down
```

Access at: http://localhost:8080

**Benefits:**
- ✅ Datasets automatically mounted at `/datasets`
- ✅ Persistent data in `label_studio/data/`
- ✅ Simple start/stop commands
- ✅ No complex volume configuration needed

### Option 2: Docker (Manual)

```bash
# Pull and run Label Studio
docker run -it -p 8080:8080 \
    -v $(pwd)/label-studio-data:/label-studio/data \
    heartexlabs/label-studio:latest
```

Access at: http://localhost:8080

### Option 3: pip install

```bash
pip install label-studio
label-studio start
```

### Option 4: Managed Service

Use Label Studio Cloud: https://app.heartex.com/

---

## Create Annotation Project

### Step 1: Create New Project

1. Open Label Studio (http://localhost:8080)
2. Click **"Create Project"**
3. Name: `fototrampeo_bosque_v1`
4. Description: Add relevant info (camera location, date range, etc.)

### Step 2: Import Images

**Method A: Use Mounted Datasets (Docker Compose - Recommended)**

If you started Label Studio with `docker compose`, your datasets are already mounted!

In Label Studio:
- Go to **Settings** → **Cloud Storage**
- Click **Add Source Storage** → **Local files**
- Path: `/datasets/fototrampeo_bosque/images`
- Click **Add Storage**
- Click **Sync Storage** to import images

That's it! All images are now available.

**Method B: Local Storage (Manual Docker)**

If using manual Docker setup:

```bash
# Copy images to Label Studio data directory
mkdir -p label-studio-data/fototrampeo_bosque
cp datasets/fototrampeo_bosque/images/* label-studio-data/fototrampeo_bosque/
```

In Label Studio:
- Go to **Settings** → **Cloud Storage**
- Add **Local Files** storage
- Path: `/label-studio/data/fototrampeo_bosque`

**Method C: Import from Cloud**

Support for:
- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- Custom HTTP server

**Method D: Upload Directly**

- Drag and drop images in the import tab
- Note: Not recommended for large datasets (2000+ images)

### Step 3: Configure Labeling Interface

1. Go to **Settings** → **Labeling Interface**
2. Click **"Code"** (XML editor)
3. Copy the contents of `label_studio/label_studio_config.xml`:

```xml
<View>
  <Image name="image" value="$image"/>
  <RectangleLabels name="label" toName="image">
    <Label value="bird" background="#FF6B6B"/>
    <Label value="wild_boar" background="#4ECDC4"/>
    <Label value="rabbit" background="#45B7D1"/>
    <Label value="roe_deer" background="#96CEB4"/>
    <Label value="fox" background="#FFEAA7"/>
    <Label value="human" background="#DFE6E9"/>
    <Label value="vehicle" background="#636E72"/>
    <Label value="unknown_animal" background="#A29BFE"/>
  </RectangleLabels>
  
  <Choices name="gender" toName="image" choice="single-radio" showInline="true">
    <Choice value="male"/>
    <Choice value="female"/>
    <Choice value="unknown_gender"/>
  </Choices>
  
  <Choices name="age_class" toName="image" choice="single-radio" showInline="true">
    <Choice value="juvenile"/>
    <Choice value="adult"/>
    <Choice value="unknown_age"/>
  </Choices>
  
  <Choices name="time_of_day" toName="image" choice="single-radio" showInline="true">
    <Choice value="day"/>
    <Choice value="night"/>
    <Choice value="dawn_dusk"/>
  </Choices>
  
  <Choices name="behavior" toName="image" choice="multiple">
    <Choice value="foraging"/>
    <Choice value="moving"/>
    <Choice value="resting"/>
    <Choice value="alert"/>
    <Choice value="grooming"/>
    <Choice value="interacting"/>
  </Choices>
  
  <Choices name="visibility" toName="image" choice="single-radio" showInline="true">
    <Choice value="clear"/>
    <Choice value="partially_occluded"/>
    <Choice value="heavily_occluded"/>
    <Choice value="motion_blur"/>
  </Choices>
  
  <TextArea name="notes" toName="image" placeholder="Additional observations..." rows="2"/>
</View>
```

4. Click **Save**

---

## Annotate Images

### Annotation Guidelines

#### 1. Drawing Bounding Boxes

- Click and drag to create a box around the animal
- Include the **entire visible animal** (even if partially occluded)
- Keep boxes **tight** around the animal (minimize background)
- For **multiple animals** of the same species: draw separate boxes

#### 2. Handling Edge Cases

**Partially visible animals:**
- ✓ Annotate if > 30% of animal is visible
- ✗ Skip if < 30% visible

**Occluded animals:**
- Draw box around visible portions
- Mark visibility as "partially_occluded" or "heavily_occluded"

**Motion blur:**
- Still annotate if animal is recognizable
- Mark visibility as "motion_blur"

**Uncertain species:**
- Use "unknown_animal" class
- Add details in notes field

**Empty images (no animals):**
- Submit without any boxes (creates empty label file)

#### 3. Attributes

Fill in additional attributes when possible:
- **Gender**: Only if clearly visible
- **Age class**: juvenile vs adult
- **Time of day**: Check image EXIF or filename timestamp
- **Behavior**: Select all applicable behaviors
- **Visibility**: Indicates image/annotation quality

#### 4. Keyboard Shortcuts

- `Ctrl + Enter`: Submit and move to next
- `Ctrl + Backspace`: Skip task
- `Delete`: Remove selected box
- `Ctrl + Z`: Undo
- `Ctrl + Shift + Z`: Redo
- Number keys `1-8`: Select class label

### Multi-User Workflow

**For teams with multiple annotators:**

1. **Assign tasks:**
   - Settings → Instructions → Add annotator guidelines
   - Distribute tasks by annotator

2. **Quality control:**
   - Enable **Review mode** in Settings
   - Senior annotator reviews submissions
   - Can accept/reject annotations

3. **Consensus:**
   - Have 2-3 annotators label the same 100 images
   - Compare inter-annotator agreement
   - Adjust guidelines if needed

---

## Export and Convert

### Step 1: Export from Label Studio

1. Go to **Export** tab
2. Select format: **JSON**
3. Download as `fototrampeo_bosque_export.json`

### Step 2: Convert to YOLO Format

```bash
python -m label_studio.converter \
    --json /path/to/fototrampeo_bosque_export.json \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt \
    --skip-duplicates
```

**Options:**
- `--json`: Path to Label Studio JSON export
- `--images`: Directory containing source images
- `--labels`: Output directory for YOLO label files
- `--classes`: Path to classes.txt file
- `--skip-duplicates`: Detect and skip duplicate images (default: True)

**Output:**
- Creates `.txt` files in `labels/` directory
- One `.txt` file per image
- YOLO format: `class_id cx cy w h` (normalized coordinates)
- Empty `.txt` for images with no annotations

### Step 3: Verify Conversion

```bash
# Check label files created
ls datasets/fototrampeo_bosque/labels/*.txt | wc -l

# View a sample label
head datasets/fototrampeo_bosque/labels/20210319_200431.txt
```

Expected output:
```
1 0.512345 0.345678 0.123456 0.234567
1 0.712345 0.545678 0.103456 0.204567
```

---

## Validate Dataset

Before training, validate your annotations:

```bash
python -m label_studio.validator \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt
```

**Sample Output:**

```
============================================================
YOLO Dataset Validation Report
============================================================

Overview:
  Total images: 2000
  Images with annotations: 1847
  Empty images: 153
  Total annotations: 3421
  Average annotations per image: 1.71

Class Distribution:
  bird                 | Boxes:   412 ( 12.0%) | Images:  389
  wild_boar            | Boxes:  1205 ( 35.2%) | Images:  892
  rabbit               | Boxes:   687 ( 20.1%) | Images:  534
  roe_deer             | Boxes:   821 ( 24.0%) | Images:  678
  fox                  | Boxes:   214 (  6.3%) | Images:  189
  human                | Boxes:    45 (  1.3%) | Images:   42
  vehicle              | Boxes:    12 (  0.4%) | Images:   11
  unknown_animal       | Boxes:    25 (  0.7%) | Images:   23

Bounding Box Size Distribution:
  Tiny       (< 1.0%):   123 (  3.6%)
  Small      (< 5.0%):   892 ( 26.1%)
  Medium     (<20.0%):  1987 ( 58.1%)
  Large      (<100%):    419 ( 12.2%)

✓ No warnings detected
```

**Save report to file:**

```bash
python -m label_studio.validator \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt \
    --output validation_report.txt
```

---

## Split Dataset

Split your dataset into train/val/test sets:

```bash
python -m yolo.split_dataset --dataset fototrampeo_bosque
```

**Default split:**
- Train: 70%
- Validation: 15%
- Test: 15%

**Result structure:**
```
datasets/fototrampeo_bosque/
├── images/          # Original images (preserved)
├── labels/          # Original labels (preserved)
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

**Note:** The split creates **copies**, so original `images/` and `labels/` directories remain intact.

---

## Train Model

After splitting, train your YOLOv11 model:

```bash
python -m yolo.train_model
```

See [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for detailed training instructions.

---

## Advanced Features

### Adding New Classes

1. **Update `classes.txt`:**

```bash
echo "badger" >> datasets/fototrampeo_bosque/labels/classes.txt
echo "deer" >> datasets/fototrampeo_bosque/labels/classes.txt
```

2. **Update Label Studio config:**
   - Go to Settings → Labeling Interface
   - Add new `<Label>` entries in the XML
   - Choose different colors for each class

3. **Re-export and convert** annotations

### Incremental Annotation

**Scenario:** You have 500 annotated images and add 300 new ones.

1. **Keep existing labels intact** in `labels/` directory

2. **Import only new images** to Label Studio

3. **Export and convert** new annotations:

```bash
python -m label_studio.converter \
    --json new_batch_export.json \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt
```

The converter will add new label files without overwriting existing ones.

### Pre-labeling with Existing Model

Speed up annotation using model predictions:

1. **Run detection** on new images:

```bash
python main.py --mode detect \
    --dataset datasets/fototrampeo_bosque_new/images \
    --output prelabels.json
```

2. **Convert predictions to Label Studio format:**

```python
# Custom script (to be implemented)
python tools/yolo_to_label_studio.py prelabels.json > import.json
```

3. **Import predictions** into Label Studio
4. Annotators **review and correct** instead of starting from scratch

### Versioning Datasets

**Recommended structure:**

```
datasets/
├── fototrampeo_bosque_v1/      # Initial 2000 images
├── fototrampeo_bosque_v2/      # Added 1000 more
└── fototrampeo_bosque_v3/      # Refined annotations
```

**Track changes:**

```bash
# Commit annotations to Git
git add datasets/fototrampeo_bosque_v1/labels/
git commit -m "Initial annotation batch: 2000 images"
```

For large files, consider **Git LFS**:

```bash
git lfs track "datasets/**/*.txt"
git lfs track "datasets/**/*.jpg"
```

---

## Troubleshooting

### Issue: Conversion fails with "Image not found"

**Cause:** Image filename mismatch between Label Studio and local files.

**Solution:**
- Ensure image filenames in JSON export match files in `images/` directory
- Check for case sensitivity (`.JPG` vs `.jpg`)
- The converter handles common extensions automatically

### Issue: Invalid bounding box coordinates

**Cause:** Boxes drawn outside image boundaries or zero-size boxes.

**Solution:**
- Re-annotate problematic images
- Run validation to identify issues:

```bash
python -m label_studio.validator ... 2>&1 | grep "Invalid"
```

### Issue: Duplicate images detected

**Cause:** Same image imported multiple times.

**Solution:**
- Use `--skip-duplicates` flag (default)
- Remove duplicates from Label Studio before export

### Issue: Classes don't match

**Cause:** Label Studio config uses different class names than `classes.txt`.

**Solution:**
- Ensure class names in XML config **exactly match** `classes.txt`
- Order doesn't matter, but spelling must be identical

### Issue: Empty label files for annotated images

**Cause:** Annotations not saved or export incomplete.

**Solution:**
- Check that annotations were **submitted** (not just saved as draft)
- Re-export from Label Studio
- Verify JSON export contains `"annotations"` field

---

## Best Practices

### 1. Annotation Quality

- **Consistency is key**: Use same rules for all images
- **Document decisions**: Keep annotation guidelines updated
- **Regular reviews**: Check 10% of annotations weekly
- **Blind QA**: Have someone re-annotate a sample without seeing original

### 2. Dataset Balance

- **Monitor class distribution** during annotation
- If class imbalance > 10:1, consider:
  - Collecting more images of rare classes
  - Data augmentation during training
  - Weighted loss functions

### 3. Version Control

- **Commit after each batch** (e.g., every 200 images)
- **Tag releases**: `git tag v1.0-annotations`
- **Document changes** in CHANGELOG.md

### 4. Backup Strategy

- **Daily exports** from Label Studio
- **Store exports** in separate location
- **Cloud backup** for critical datasets

---

## References

- [Label Studio Documentation](https://labelstud.io/guide/)
- [YOLOv11 Documentation](https://docs.ultralytics.com/)
- [YOLO Format Specification](https://docs.ultralytics.com/datasets/detect/)
- [AnimalDetector Training Guide](TRAINING_GUIDE.md)

---

## Support

For issues or questions:
1. Check [TRAINING_FAQ.md](TRAINING_FAQ.md)
2. Review Label Studio docs
3. Open an issue in this repository

---

**Last updated:** 2025-11-03


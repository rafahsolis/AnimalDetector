# Migrating Existing Dataset to Label Studio Workflow

## Current Situation

Your `fototrampeo_bosque` dataset currently has this structure:

```
datasets/fototrampeo_bosque/
├── 20210319_200431.JPG
├── 20210319_200432.JPG
├── ... (1933 images in root)
├── images/ (subdirectory with additional images)
├── labels/
│   └── classes.txt
└── yolo_dataset/
```

## Target Structure

To use the Label Studio workflow, reorganize to:

```
datasets/fototrampeo_bosque/
├── images/              # All source images here
├── labels/              # YOLO annotations here
│   └── classes.txt
├── train/               # Created by split_dataset.py
├── val/
├── test/
└── data.yaml            # Created by generate_data_yaml.py
```

## Migration Steps

### Option 1: Reorganize Existing Dataset

```bash
cd /home/rafa/PycharmProjects/AnimalDetector/datasets/fototrampeo_bosque

# Move all JPG files from root to images/ directory
find . -maxdepth 1 -name "*.JPG" -o -name "*.jpg" | while read file; do
    mv "$file" images/
done

# Verify
ls images/*.JPG | wc -l  # Should show total count
ls *.JPG 2>/dev/null     # Should show "No such file"

# Now your dataset is ready for Label Studio workflow
```

### Option 2: Create New Dataset for Label Studio

Keep existing dataset as-is and create a new one:

```bash
# Initialize new dataset
python -m label_studio.init_dataset fototrampeo_bosque_v2

# Copy images
cp datasets/fototrampeo_bosque/images/*.JPG datasets/fototrampeo_bosque_v2/images/

# Or if images are still in root:
cp datasets/fototrampeo_bosque/*.JPG datasets/fototrampeo_bosque_v2/images/

# Copy classes if you want same classes
cp datasets/fototrampeo_bosque/labels/classes.txt \
   datasets/fototrampeo_bosque_v2/labels/classes.txt
```

## After Reorganization

Once images are in `images/` directory:

### 1. Set up Label Studio

```bash
# Start Label Studio with Docker
docker run -it -p 8080:8080 \
    -v $(pwd)/label-studio-data:/label-studio/data \
    heartexlabs/label-studio:latest

# Access at http://localhost:8080
```

### 2. Create Project in Label Studio

1. Create new project: "fototrampeo_bosque"
2. Go to Settings → Labeling Interface
3. Copy contents from `label_studio/label_studio_config.xml`
4. Save

### 3. Import Images

**Method A: Via Local Storage (Docker)**

```bash
# Copy images to Label Studio data directory
mkdir -p label-studio-data/fototrampeo_bosque_images
cp datasets/fototrampeo_bosque/images/*.JPG label-studio-data/fototrampeo_bosque_images/
```

In Label Studio:
- Settings → Cloud Storage → Add Local Files
- Path: `/label-studio/data/fototrampeo_bosque_images`
- Sync

**Method B: Upload Directly**

- Go to your project
- Click "Import"
- Drag and drop images (good for < 500 images)
- For 1933 images, use Method A

### 4. Annotate

Draw bounding boxes around animals in each image.

See [LABEL_STUDIO_GUIDE.md](LABEL_STUDIO_GUIDE.md) for detailed annotation guidelines.

### 5. Export from Label Studio

1. Go to Export tab
2. Select format: JSON
3. Download → save as `fototrampeo_bosque_export.json`

### 6. Convert to YOLO Format

```bash
python -m label_studio.converter \
    --json fototrampeo_bosque_export.json \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt
```

This creates `.txt` files in `labels/` directory with YOLO format annotations.

### 7. Validate Annotations

```bash
python -m label_studio.validator \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt
```

### 8. Split Dataset

```bash
python -m yolo.split_dataset --dataset fototrampeo_bosque
```

Creates `train/`, `val/`, `test/` directories.

### 9. Generate Training Config

```bash
python -m yolo.generate_data_yaml --dataset fototrampeo_bosque
```

Creates `data.yaml` for YOLOv11.

### 10. Train Model

```bash
python -m yolo.train_model
```

## Quick Reorganization Script

Save this as `reorganize_dataset.sh`:

```bash
#!/bin/bash

DATASET="fototrampeo_bosque"
DATASET_DIR="datasets/$DATASET"

echo "Reorganizing $DATASET dataset..."

# Check if images directory exists
if [ ! -d "$DATASET_DIR/images" ]; then
    echo "Creating images directory..."
    mkdir -p "$DATASET_DIR/images"
fi

# Move all JPG/jpg files from root to images/
echo "Moving images to images/ directory..."
find "$DATASET_DIR" -maxdepth 1 \( -name "*.JPG" -o -name "*.jpg" \) -exec mv {} "$DATASET_DIR/images/" \;

# Count images
IMAGE_COUNT=$(ls "$DATASET_DIR/images/"*.{JPG,jpg} 2>/dev/null | wc -l)
echo "✓ Reorganization complete!"
echo "  Total images in images/: $IMAGE_COUNT"

# Check if labels directory exists
if [ ! -d "$DATASET_DIR/labels" ]; then
    echo "Creating labels directory..."
    mkdir -p "$DATASET_DIR/labels"
fi

# Check if classes.txt exists
if [ ! -f "$DATASET_DIR/labels/classes.txt" ]; then
    echo "Creating default classes.txt..."
    cat > "$DATASET_DIR/labels/classes.txt" << EOF
bird
wild_boar
rabbit
roe_deer
fox
human
vehicle
unknown_animal
EOF
    echo "✓ Created classes.txt with default animal classes"
fi

echo ""
echo "Next steps:"
echo "1. Start Label Studio: docker run -it -p 8080:8080 -v \$(pwd)/label-studio-data:/label-studio/data heartexlabs/label-studio:latest"
echo "2. Follow guide: docs/LABEL_STUDIO_GUIDE.md"
```

Make executable and run:

```bash
chmod +x reorganize_dataset.sh
./reorganize_dataset.sh
```

## Troubleshooting

### Images in Multiple Locations

If you have images both in root and in `images/` subdirectory:

```bash
# Count images in each location
ls datasets/fototrampeo_bosque/*.JPG 2>/dev/null | wc -l
ls datasets/fototrampeo_bosque/images/*.JPG 2>/dev/null | wc -l

# Move only root-level images
find datasets/fototrampeo_bosque -maxdepth 1 -name "*.JPG" -exec mv {} datasets/fototrampeo_bosque/images/ \;
```

### Check for Duplicates

```bash
# Find duplicate filenames (not content)
cd datasets/fototrampeo_bosque
find images/ -type f -name "*.JPG" -printf "%f\n" | sort | uniq -d
```

## See Also

- [LABEL_STUDIO_GUIDE.md](LABEL_STUDIO_GUIDE.md) - Complete annotation guide
- [LABEL_STUDIO_QUICK_REF.md](LABEL_STUDIO_QUICK_REF.md) - Command reference
- [LABEL_STUDIO_IMPLEMENTATION.md](LABEL_STUDIO_IMPLEMENTATION.md) - Technical details


# Docker Compose Integration - Complete ✅

## Summary

Simplified Label Studio setup with Docker Compose for easier workflow.

## What Was Created

### 1. Docker Compose Configuration
**File:** `label_studio/docker compose.yml`

Features:
- ✅ Automatic dataset mounting (`../datasets` → `/datasets`)
- ✅ Persistent data storage (`./data` → Label Studio database)
- ✅ Pre-configured environment variables
- ✅ Auto-restart unless stopped
- ✅ Standard port 8080

### 2. Dedicated README
**File:** `label_studio/README.md`

Complete guide including:
- Quick start (3 commands)
- First-time setup instructions
- Daily usage commands
- Full annotation workflow
- Troubleshooting section

### 3. Updated Documentation
**Files Updated:**
- `LABEL_STUDIO_SETUP.md` - Simplified Quick Start
- `docs/LABEL_STUDIO_GUIDE.md` - Docker Compose as Option 1
- `docs/LABEL_STUDIO_QUICK_REF.md` - Docker Compose commands first

## New Workflow

### Super Simple - Just 3 Commands!

```bash
# 1. Start Label Studio
cd label_studio
docker compose up -d

# 2. Annotate
# Open http://localhost:8080
# Create project, import from /datasets/fototrampeo_bosque/images

# 3. Convert to YOLO
python -m label_studio.converter \
    --json export.json \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt
```

## Before vs After

### Before (Complex)
```bash
# Complex Docker command with volume mounts
docker run -it -p 8080:8080 \
    -v $(pwd)/label-studio-data:/label-studio/data \
    -v $(pwd)/datasets:/datasets \
    -e LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true \
    -e LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/datasets \
    --name label-studio \
    heartexlabs/label-studio:latest

# Then copy images or configure paths...
```

### After (Simple)
```bash
# Single command!
cd label_studio && docker compose up -d

# Datasets already mounted at /datasets
# Just point to /datasets/fototrampeo_bosque/images
```

## Benefits

### 1. **Simplicity**
- One command to start: `docker compose up -d`
- One command to stop: `docker compose down`
- No complex Docker arguments to remember

### 2. **Automatic Dataset Mounting**
- All datasets in `../datasets` automatically available
- Access as `/datasets/fototrampeo_bosque/images`
- Read-only mount for safety

### 3. **Persistent Data**
- All Label Studio data in `label_studio/data/`
- Survives container restarts
- Easy to backup: just tar the `data/` folder

### 4. **Pre-configured**
- Environment variables already set
- Local files serving enabled
- Document root configured

### 5. **Easy Management**
```bash
# Start
docker compose up -d

# Stop
docker compose down

# Restart
docker compose restart

# View logs
docker compose logs -f

# Full reset
docker compose down -v
rm -rf data/
```

## File Structure

```
label_studio/
├── docker compose.yml       # Docker Compose configuration
├── README.md                # Complete usage guide
├── label_studio_config.xml  # UI configuration
├── data/                    # Label Studio data (auto-created)
│   ├── media/
│   └── label_studio.sqlite3
├── converter.py             # Tools
├── validator.py
└── init_dataset.py

../datasets/                 # Mounted at /datasets in container
├── fototrampeo_bosque/
│   ├── images/              # Access as /datasets/fototrampeo_bosque/images
│   └── labels/
└── other_dataset/
```

## Quick Start Instructions

**For users:**

See `label_studio/README.md` - it has everything needed:
- Start command
- Browser setup
- Image import
- Export and conversion
- Complete workflow

## Example Session

```bash
# Terminal 1: Start Label Studio
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose up -d

# Terminal 2: Wait a few seconds, then open browser
firefox http://localhost:8080

# In browser:
# 1. Create account
# 2. Create project "fototrampeo_bosque"
# 3. Settings → Labeling Interface → paste XML config
# 4. Settings → Cloud Storage → Add Local Files
#    Path: /datasets/fototrampeo_bosque/images
# 5. Click "Sync Storage"
# 6. Start annotating!

# After annotating, export as JSON

# Terminal 2: Convert
cd /home/rafa/PycharmProjects/AnimalDetector
python -m label_studio.converter \
    --json export.json \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt

# Validate
python -m label_studio.validator \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt

# Train
python -m yolo.split_dataset --dataset fototrampeo_bosque
python -m yolo.generate_data_yaml --dataset fototrampeo_bosque
python -m yolo.train_model
```

## Troubleshooting

### Port 8080 in use?
Edit `docker compose.yml`:
```yaml
ports:
  - "8081:8080"  # Change to 8081
```

### Can't see datasets?
- Check path: `/datasets/fototrampeo_bosque/images` (not `../datasets`)
- Click "Sync Storage" button
- Check logs: `docker compose logs`

### Need to reset?
```bash
docker compose down -v
rm -rf data/
docker compose up -d
```

## Documentation Updates

All docs now mention Docker Compose as the recommended method:

✅ `LABEL_STUDIO_SETUP.md` - Updated Quick Start  
✅ `docs/LABEL_STUDIO_GUIDE.md` - Docker Compose as Option 1  
✅ `docs/LABEL_STUDIO_QUICK_REF.md` - Docker Compose commands first  
✅ `label_studio/README.md` - New dedicated guide  

## Status

**Docker Compose Setup:** ✅ Complete  
**Documentation Updated:** ✅ All files  
**Tested:** ✅ Configuration valid  
**Ready to Use:** ✅ Yes  

---

**Created:** November 3, 2025  
**Purpose:** Simplify Label Studio startup  
**Result:** 1 command instead of complex Docker CLI  
**User Feedback:** Implemented based on user request for simpler workflow


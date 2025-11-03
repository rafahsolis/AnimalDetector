# Label Studio for Animal Detector

Simple Docker Compose setup for annotating camera trap images.

## Quick Start

```bash
# Start Label Studio
cd label_studio
docker compose up -d

# Open browser
firefox http://localhost:8080
```

That's it! Your datasets are already mounted and accessible.

## First Time Setup

### 1. Prepare Data Directory
```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
mkdir -p data
chmod 755 data
```

### 2. Start Label Studio
```bash
docker compose up -d
```

**Note:** If you get permission errors, the data directory will be created automatically but you may need to fix permissions:
```bash
sudo chown -R $USER:$USER data/
```

### 3. Open Browser
Open: http://localhost:8080

### 4. Create Account (First Time Only)

**Important:** Label Studio has **NO default credentials**. You must create an account on first use.

- You'll see a **Sign Up** page (not login!)
- Enter your email (can be anything, e.g., `user@localhost`)
- Set a password (remember this!)
- Click **Create Account**

**On subsequent visits:**
- Use the same email and password you created
- If you forgot your password, see [Reset Password](#reset-password) below

### 5. Create Project
- Click "Create Project"
- Name: `fototrampeo_bosque`
- Click "Save"

### 6. Configure Labeling Interface
- Go to **Settings** → **Labeling Interface**
- Click **Code** (top right)
- Copy and paste the entire contents from `label_studio_config.xml` (in this folder)
- Click **Save**

**What this configuration includes:**
- **8 animal classes** with color-coded labels (bird, wild_boar, rabbit, etc.)
- **Per-animal attributes** (linked to each bounding box):
  - Gender: male, female, unknown
  - Age class: juvenile, adult, unknown
  - Visibility: clear, partially occluded, heavily occluded, motion blur
  - Behavior: foraging, moving, resting, etc. (multi-select)
- **Image-level attributes** (for the whole image):
  - Time of day: day, night, dawn/dusk
  - Notes: free text for observations

When you annotate, you can set different attributes for each animal in the image!

### 7. Import Images
- Go to **Settings** → **Cloud Storage**
- Click **Add Source Storage** → **Local files**
- Path: `/datasets/fototrampeo_bosque/images`
- Click **Add Storage**
- Click **Sync Storage** to import images

## Daily Usage

```bash
# Start
cd label_studio
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f

# Restart
docker compose restart
```

## Annotation Workflow

### 1. Annotate Images
- Open your project
- Click on an image
- Draw bounding boxes around animals
- Select the class (bird, wild_boar, etc.)
- Fill in metadata (optional): gender, age, behavior
- Click **Submit**
- Continue with next image

### 2. Export Annotations
- Go to **Export** tab
- Select format: **JSON**
- Click **Export**
- Save as `export.json`

### 3. Convert to YOLO Format
```bash
cd /home/rafa/PycharmProjects/AnimalDetector

python -m label_studio.converter \
    --json export.json \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt
```

### 4. Validate Annotations
```bash
python -m label_studio.validator \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt
```

### 5. Train Model
```bash
# Split dataset
python -m yolo.split_dataset --dataset fototrampeo_bosque

# Generate config
python -m yolo.generate_data_yaml --dataset fototrampeo_bosque

# Train
python -m yolo.train_model
```

## Features

✅ **Datasets auto-mounted** - All datasets in `../datasets` are accessible  
✅ **Persistent data** - Annotations saved in `./data` directory  
✅ **Easy start/stop** - Simple docker compose commands  
✅ **Multi-dataset support** - Switch between datasets easily  
✅ **Port 8080** - Standard Label Studio port  

## Folder Structure

```
label_studio/
├── docker compose.yml       # This file - defines the setup
├── label_studio_config.xml  # UI configuration for annotation
├── data/                    # Label Studio data (auto-created)
│   ├── media/               # Uploaded files
│   └── label_studio.sqlite3 # Database
├── converter.py             # JSON → YOLO converter
├── validator.py             # Dataset validator
└── init_dataset.py          # Dataset initializer

../datasets/                 # Your datasets (mounted read-only)
├── fototrampeo_bosque/
│   ├── images/              # Your images
│   └── labels/              # YOLO annotations
└── other_dataset/
```

## Accessing Your Images

When adding cloud storage in Label Studio:
- **Path:** `/datasets/fototrampeo_bosque/images`
- **Or:** `/datasets/other_dataset/images`

The `/datasets` path inside the container points to your `../datasets` folder.

## Troubleshooting

### Can't Login / Forgot Password?

**Label Studio has NO default credentials!** You create your own account on first use.

**If you see a login page but can't get in:**

1. **Never created an account?** Look for "Sign Up" or "Create Account" link
2. **Forgot password?** Reset it:

```bash
# Stop Label Studio
cd label_studio
docker compose down

# Reset the database (WARNING: deletes all data!)
rm -rf data/

# Restart fresh
docker compose up -d

# Open browser - you'll see Sign Up page again
firefox http://localhost:8080
```

**To change password without losing data:**

```bash
# Access the container
docker compose exec label-studio bash

# Inside container, run Django command
python /label-studio/label_studio/manage.py changepassword your-email@localhost

# Exit container
exit
```

### Port 8080 already in use?
Edit `docker compose.yml`:
```yaml
ports:
  - "8081:8080"  # Use port 8081 instead
```

### Container won't start?
```bash
# Check logs
docker compose logs

# Remove and recreate
docker compose down
docker compose up -d
```

### Can't see images?
- Make sure images are in `datasets/fototrampeo_bosque/images/`
- Check path in Cloud Storage settings: `/datasets/fototrampeo_bosque/images`
- Click "Sync Storage" button

### Reset everything?
```bash
# Stop and remove everything
docker compose down -v

# Remove data directory
rm -rf data/

# Start fresh
docker compose up -d
```

## Backup Your Work

Your annotations are in `./data/`. To backup:

```bash
# Backup Label Studio data
tar -czf label-studio-backup-$(date +%Y%m%d).tar.gz data/

# Or just export from the UI regularly
# Export → JSON → Download
```

## Complete Documentation

For more details, see:
- **Login issues?** `LOGIN_GUIDE.md` (authentication, password reset)
- **Configuration explained:** `CONFIG_GUIDE.md` (detailed explanation of label_studio_config.xml)
- **Complete guide:** `../docs/LABEL_STUDIO_GUIDE.md`
- **Quick reference:** `../docs/LABEL_STUDIO_QUICK_REF.md`
- **Main README:** `../LABEL_STUDIO_SETUP.md`

## Support

Questions? Check the docs above or the main documentation in `../docs/`.

---

**TL;DR - Just run:**
```bash
cd label_studio && docker compose up -d
```
Then open http://localhost:8080 🚀


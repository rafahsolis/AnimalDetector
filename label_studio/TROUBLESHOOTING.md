# Label Studio Troubleshooting Guide

## Problem: Can't See Images in Label Studio

This is the most common issue when starting a new project. Here's how to fix it:

### Solution: Configure Local Storage

Label Studio needs to be told **where to find your images** inside the Docker container.

#### Step-by-Step Fix

1. **Open your project in Label Studio**
   - Go to http://localhost:8080
   - Click on your project (e.g., "fototrampeo_bosque")

2. **Go to Settings → Cloud Storage**
   - Click the **⚙️ Settings** button (top right)
   - Click **Cloud Storage** in the left sidebar

3. **Add Source Storage**
   - Click **Add Source Storage**
   - Select **Local files**

4. **Configure the path** (IMPORTANT!)
   - **Storage Title:** `fototrampeo_bosque_images` (or any name)
   - **Absolute local path:** `/datasets/fototrampeo_bosque/images`
   - **File Filter Regex:** `.*\.(jpg|jpeg|png|JPG|JPEG|PNG)$`
   - ✅ Check **Treat every bucket object as a source file**
   - Click **Add Storage**

5. **Sync the storage**
   - After adding, you'll see your storage in the list
   - Click the **Sync** button (🔄 icon) next to your storage
   - Wait for sync to complete (should take a few seconds)

6. **Go back to your project**
   - Click on the project name to exit settings
   - You should now see all your images!

### Why This Path?

The Docker container mounts your datasets at `/datasets`:

```yaml
volumes:
  - ../datasets:/datasets:ro
```

So:
- ❌ Don't use: `/home/rafa/PycharmProjects/AnimalDetector/datasets/...` (host path)
- ✅ Use: `/datasets/fototrampeo_bosque/images` (container path)

## Common Issues

### Issue 1: "No tasks found"

**Cause:** Storage not synced or wrong path

**Fix:**
1. Go to Settings → Cloud Storage
2. Click **Sync** button (🔄) next to your storage
3. Check the path is `/datasets/...` not your host path

### Issue 2: "Permission denied" errors in logs

**Cause:** File permissions issue

**Fix:**
```bash
cd /home/rafa/PycharmProjects/AnimalDetector
chmod -R 755 datasets/fototrampeo_bosque/images
```

Or check Docker logs:
```bash
cd label_studio
docker compose logs -f
```

### Issue 3: Images show broken/not loading

**Cause:** Environment variables not set properly

**Check docker-compose.yml has:**
```yaml
environment:
  - LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
  - LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/datasets
```

If not, fix it and restart:
```bash
docker compose down
docker compose up -d
```

### Issue 4: Storage configuration is lost after restart

**Cause:** Label Studio data directory not persistent

**Fix:** Make sure `label_studio/data` directory exists and is mounted:
```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
mkdir -p data
chmod 755 data
docker compose down
docker compose up -d
```

### Issue 5: Can add storage but sync fails

**Cause:** Images directory doesn't exist or is empty

**Check:**
```bash
ls -la /home/rafa/PycharmProjects/AnimalDetector/datasets/fototrampeo_bosque/images
```

Should show `.jpg` or `.JPG` files.

## Verification Checklist

Use this checklist to verify everything is working:

- [ ] Docker container is running: `docker compose ps`
- [ ] Can access Label Studio: http://localhost:8080
- [ ] Images exist on host: `ls datasets/fototrampeo_bosque/images/*.JPG | head`
- [ ] Datasets mounted in container: `docker exec animal-detector-label-studio ls /datasets/fototrampeo_bosque/images | head`
- [ ] Environment variables set: `docker exec animal-detector-label-studio env | grep LABEL_STUDIO_LOCAL`
- [ ] Storage configured in Settings → Cloud Storage
- [ ] Storage synced (green checkmark)
- [ ] Tasks visible in project

## Quick Verification Commands

```bash
# 1. Check container status
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose ps

# 2. Check images exist (host)
ls -lh ../datasets/fototrampeo_bosque/images/*.JPG | head -5

# 3. Check images visible in container
docker exec animal-detector-label-studio ls -lh /datasets/fototrampeo_bosque/images | head -5

# 4. Check environment variables
docker exec animal-detector-label-studio env | grep LABEL_STUDIO

# 5. View logs for errors
docker compose logs --tail=100 | grep -i error
```

## Still Not Working?

### Get detailed logs:

```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose logs -f
```

### Restart from scratch:

```bash
# Stop container
docker compose down

# Check docker-compose.yml is correct
cat docker-compose.yml

# Start fresh
docker compose up -d

# Watch logs
docker compose logs -f
```

### Test manual import (alternative):

If local storage still doesn't work, you can manually import images:

1. Go to your project
2. Click **Import**
3. Click **Upload Files**
4. Select images from your computer
5. Click **Import**

**Note:** This copies images into Label Studio, using more disk space.

## Need More Help?

1. Check Label Studio docs: https://labelstud.io/guide/storage.html
2. Check project logs: `docker compose logs -f`
3. Verify paths in docker-compose.yml
4. Make sure container can access `/datasets` mount


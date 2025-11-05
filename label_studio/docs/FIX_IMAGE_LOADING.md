# Fix: Images Won't Load in Label Studio

## Problem
You see the list of images in Label Studio, but when you click on one, you get:
```
There was an issue loading URL from $image value
URL: /data/local-files/?d=fototrampeo_bosque/images/...
```

## Solution (2 Steps)

### Step 1: Restart Containers
The docker-compose.yml has been updated with proper CORS settings. Restart to apply:

```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose down
docker compose up -d
```

**Wait 10-15 seconds** for Label Studio to fully start.

### Step 2: Clear Browser Cache
- **Option A:** Hard reload: `Ctrl + Shift + R` (Linux/Windows) or `Cmd + Shift + R` (Mac)
- **Option B:** Use incognito/private browsing mode
- **Option C:** Clear browser cache in settings

### Step 3: Test
1. Go to http://localhost:8080
2. Open your project
3. Click on any image
4. Image should now load! ✅

## What Was Fixed?

Updated `docker-compose.yml` with:
```yaml
- LABEL_STUDIO_HOSTNAME=http://localhost:8080
- LABEL_STUDIO_HOST=
- LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
- LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/datasets
```

These settings:
- ✅ Enable local file serving
- ✅ Set correct hostname for CORS
- ✅ Allow Label Studio to access files in `/datasets`

## Still Not Working?

### Check 1: Verify container is running
```bash
docker compose ps
```

Should show both containers as "Up".

### Check 2: Verify environment variables
```bash
docker exec animal-detector-label-studio env | grep LABEL_STUDIO
```

Should show:
```
LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/datasets
LABEL_STUDIO_HOSTNAME=http://localhost:8080
```

### Check 3: Verify images are accessible
```bash
docker exec animal-detector-label-studio ls /datasets/fototrampeo_bosque/images | head
```

Should list your `.JPG` files.

### Check 4: Try a different browser
Sometimes browser extensions or settings interfere. Try:
- Different browser (Chrome, Firefox, Edge)
- Incognito/private mode
- Disable ad blockers/extensions

### Check 5: Check storage configuration in Label Studio
In Label Studio → Settings → Cloud Storage:
- Path should be: `/datasets/fototrampeo_bosque/images`
- "Treat every bucket object as a source file" should be ✅ checked
- Storage should show as "Synced" (green checkmark)

## Advanced: Accessing from Another Machine

If you want to access Label Studio from a different computer on your network:

1. Find your server's IP address:
```bash
hostname -I | awk '{print $1}'
```

2. Update docker-compose.yml:
```yaml
- LABEL_STUDIO_HOSTNAME=http://YOUR_IP:8080
```

3. Restart:
```bash
docker compose down
docker compose up -d
```

4. Access from other machine: `http://YOUR_IP:8080`

---

**Summary:** The fix is to restart containers (to load new CORS config) and clear browser cache. Images should then load properly! 🎉


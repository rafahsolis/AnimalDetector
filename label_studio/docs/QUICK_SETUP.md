# Quick Setup: Get Images Showing in Label Studio

Follow these steps **in order** to see your images:

## ✅ Step-by-Step Checklist

### 1. Verify Label Studio is Running
```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose ps
```
You should see both containers running:
- `animal-detector-label-studio`
- `animal-detector-postgres`

### 2. Open Label Studio
Open browser: http://localhost:8080

### 3. Sign Up (First Time) or Login
- **First time:** Create account with any email/password
- **Returning:** Use your previous credentials

### 4. Create a Project
- Click **"Create Project"**
- **Name:** `fototrampeo_bosque` (or any name you like)
- Click **"Save"**

### 5. Configure the Labeling Interface
- Click **⚙️ Settings** (top right)
- Click **"Labeling Interface"** (left sidebar)
- Click **"Code"** button (top right)
- Delete everything in the editor
- Copy ALL contents from `/home/rafa/PycharmProjects/AnimalDetector/label_studio/label_studio_config.xml`
- Paste into the editor
- Click **"Save"** (bottom right)

### 6. Add Cloud Storage (THIS IS THE KEY STEP!)
- Still in Settings, click **"Cloud Storage"** (left sidebar)
- Click **"Add Source Storage"**
- Select **"Local files"**
- Fill in the form:
  - **Storage Title:** `fototrampeo_images` (or any name)
  - **Absolute local path:** `/datasets/fototrampeo_bosque/images`
  - **File Filter Regex:** `.*\.(jpg|jpeg|png|JPG|JPEG|PNG)$`
  - ✅ Check **"Treat every bucket object as a source file"**
- Click **"Add Storage"**

### 7. Sync the Storage
- You should now see your storage in the list
- Click the **🔄 Sync** button next to your storage
- Wait for it to complete (green checkmark)

### 8. Exit Settings and Start Annotating!
- Click on your project name at the top
- You should now see all your images! 🎉
- Click on any image to start annotating
- If the image doesn't load, see troubleshooting below

---

## 🔍 Troubleshooting

### Images list appears but won't load?

This is a CORS/serving issue. **Solution:**

```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose down
docker compose up -d
```

Wait 10-15 seconds, then:
- Clear browser cache (or use incognito mode)
- Refresh Label Studio page
- Try clicking on an image again

The docker-compose.yml has been configured with proper CORS settings, but a restart is needed for them to take effect.

### No images appear after sync?

**Check the container can see images:**
```bash
docker exec animal-detector-label-studio ls /datasets/fototrampeo_bosque/images | head
```

You should see your `.JPG` files listed.

### Database errors?

Restart the containers:
```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose down
docker compose up -d
```

Wait 10-15 seconds, then try again.

### Wrong path error?

Make sure you use the **container path**, not the host path:
- ✅ Correct: `/datasets/fototrampeo_bosque/images`
- ❌ Wrong: `/home/rafa/PycharmProjects/AnimalDetector/datasets/...`

The datasets folder is mounted at `/datasets` inside the container.

---

## 📊 What You'll See

Once images are loaded:
- Click on any image to start annotating
- Draw bounding boxes around animals
- Select animal class (bird, wild_boar, rabbit, etc.)
- Fill in attributes (gender, age, behavior, etc.)
- Submit annotation
- Next image automatically loads

Happy annotating! 🦌🦊🐗


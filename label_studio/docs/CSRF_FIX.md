# CSRF Error Fix for Label Studio Behind Cloudflare Tunnel

## Problem
When accessing Label Studio through `https://label.montedelavilla.org`, you get:
```
Forbidden (403)
CSRF verification failed. Request aborted.
```

## Solution Steps

### 1. Update docker-compose.yml
Ensure the `label-studio` service has these environment variables:
```yaml
environment:
  - LABEL_STUDIO_HOSTNAME=https://label.montedelavilla.org
  - LABEL_STUDIO_HOST=https://label.montedelavilla.org
  - CSRF_TRUSTED_ORIGINS=https://label.montedelavilla.org
  - SSRF_PROTECTION_ENABLED=false
```

### 2. Restart Label Studio
```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose down label-studio
docker compose up -d label-studio
```

### 3. Clear Browser Data
**Important**: You must clear cookies and cache for the site.

#### Option A: Use Incognito/Private Window
The easiest solution - just open an incognito/private window and try again.

#### Option B: Clear Cookies Manually
In your browser:
1. Open Developer Tools (F12)
2. Go to Application/Storage tab
3. Find Cookies → `https://label.montedelavilla.org`
4. Delete all cookies
5. Refresh the page

### 4. Verify Environment Variables
Check that the environment variables are correctly set:
```bash
docker compose exec label-studio env | grep -E "(CSRF|HOSTNAME|HOST)"
```

You should see:
```
LABEL_STUDIO_HOSTNAME=https://label.montedelavilla.org
LABEL_STUDIO_HOST=https://label.montedelavilla.org
CSRF_TRUSTED_ORIGINS=https://label.montedelavilla.org
```

### 5. Check Label Studio Logs
If still having issues:
```bash
docker compose logs label-studio --tail=100
```

Look for errors related to CSRF or security.

## Why This Happens

Django (which Label Studio uses) has CSRF protection to prevent cross-site request forgery attacks. When you access Label Studio through a different domain than it expects, Django rejects the login form submission.

The fix tells Django to trust requests from `https://label.montedelavilla.org`.

## Still Not Working?

### Try a Full Restart
```bash
docker compose down
docker compose up -d
```

Wait 30 seconds for all services to start, then try accessing the site in an incognito window.

### Check Database Connection
```bash
docker compose logs db --tail=50
```

Make sure PostgreSQL is running properly.

### Access Locally First
Try accessing http://localhost:8080 first to create your account, then try the public URL.

## Alternative: Disable CSRF (NOT RECOMMENDED FOR PRODUCTION)
Only use this for testing:
```yaml
environment:
  - LABEL_STUDIO_CSRF_COOKIE_SECURE=false
  - LABEL_STUDIO_SESSION_COOKIE_SECURE=false
```

**Warning**: This reduces security. Only use for local testing.


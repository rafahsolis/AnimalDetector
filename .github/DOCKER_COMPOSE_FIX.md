# Docker Compose Command Fix - Complete ✅

## Issue Fixed

**Problem:** Documentation used old `docker-compose` command instead of the modern `docker compose` (without dash).

**Solution:** Updated all documentation to use `docker compose`.

## What Was Changed

### Command Updates

**Before (Old):**
```bash
docker-compose up -d
docker-compose down
docker-compose logs
docker-compose ps
```

**After (New):**
```bash
docker compose up -d
docker compose down
docker compose logs
docker compose ps
```

### Files Updated

All markdown files with docker-compose references:

1. ✅ `label_studio/README.md`
2. ✅ `docs/LABEL_STUDIO_GUIDE.md`
3. ✅ `docs/LABEL_STUDIO_QUICK_REF.md`
4. ✅ `LABEL_STUDIO_SETUP.md`
5. ✅ `DOCKER_COMPOSE_INTEGRATION.md`
6. ✅ `LABEL_STUDIO_CONFIG_FIXED.md`

### Additional Fixes

**docker-compose.yml improvements:**
- ✅ Removed obsolete `version: '3.8'` line (Docker Compose v2 doesn't need it)
- ✅ Added `user: "${UID:-1000}:${GID:-1000}"` to avoid permission issues
- ✅ Created `data/` directory with proper permissions

## Testing

### Verified Working

```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio

# Start
docker compose up -d
✓ Started successfully

# Check status
docker compose ps
✓ Container running

# Check logs
docker compose logs
✓ Label Studio initializing database

# Test accessibility
curl http://localhost:8080
✓ Accessible
```

## Permission Issue Fixed

The original error:
```
PermissionError: [Errno 13] Permission denied: '/label-studio/data/media'
```

**Fixed by:**
1. Adding `user: "${UID:-1000}:${GID:-1000}"` to docker-compose.yml
2. Pre-creating `data/` directory with correct permissions
3. Updated README with setup instructions

## Correct Usage Now

### Starting Label Studio

```bash
cd label_studio

# Create data directory (first time only)
mkdir -p data
chmod 755 data

# Start Label Studio
docker compose up -d

# Open browser
firefox http://localhost:8080
```

### Daily Commands

```bash
# Start
docker compose up -d

# Stop
docker compose down

# Restart
docker compose restart

# View logs
docker compose logs -f

# Check status
docker compose ps
```

## Why The Change?

**Docker Compose V1 vs V2:**
- **Old:** `docker-compose` (standalone Python tool)
- **New:** `docker compose` (integrated into Docker CLI)

The new version:
- ✅ No separate installation needed
- ✅ Better integration with Docker
- ✅ Modern and maintained
- ✅ No dash in the command

## Status

**Command Fixed:** ✅ All documentation updated  
**Permission Fixed:** ✅ User mapping added  
**Tested:** ✅ Label Studio starts successfully  
**Ready to Use:** ✅ Yes

## Quick Test

```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose up -d
```

Then open: http://localhost:8080

**Everything should work!** 🎉

---

**Date:** November 3, 2025  
**Fixed:** docker-compose → docker compose  
**Files Updated:** 6 markdown files  
**Status:** Complete ✓


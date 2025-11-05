# ✅ Label Studio Database Issue - RESOLVED

## Problem
You were experiencing `django.db.utils.OperationalError: database is locked` errors in Label Studio.

## Root Cause
Label Studio was using **SQLite** as the database backend. SQLite has limitations with concurrent access and file locking, especially in Docker containers with user permission mappings.

## Solution Applied
Upgraded the Label Studio setup to use **PostgreSQL** instead of SQLite.

### Changes Made:

#### 1. Updated `docker-compose.yml`
- Added PostgreSQL 15 container
- Configured Label Studio to use PostgreSQL
- Removed SQLite-related user mapping
- Added persistent volume for PostgreSQL data

#### 2. Centralized Documentation
- Moved all markdown files into `label_studio/docs/`
- Updated references accordingly

#### 3. Added Guides
- `QUICK_SETUP.md` – Fast start for image annotation
- `TROUBLESHOOTING.md` – Common issues and fixes
- `README.md` – Central hub for docs

## What to Do Now

### 1. Access Label Studio
Open: http://localhost:8080

### 2. First Time? Create Account
- Email: any email (e.g., `user@localhost`)
- Password: choose a password you'll remember

### 3. See Your Images
Follow steps in `QUICK_SETUP.md`:
1. Create project
2. Add labeling interface
3. Add cloud storage `/datasets/fototrampeo_bosque/images`
4. Sync storage

## Benefits of PostgreSQL

- ✅ No more locking errors
- ✅ Better performance
- ✅ Supports concurrent users
- ✅ Improved data integrity

## Containers

- `animal-detector-label-studio` – Web interface (port 8080)
- `animal-detector-postgres` – Database backend

## Daily Commands
```bash
cd label_studio
docker compose up -d
# ... work ...
docker compose down
```

## Data Persistence
- **DB volume:** PostgreSQL stored in named volume
- **App data:** `label_studio/data/`

## Next Steps
1. ✅ Database fixed
2. 📘 Read `QUICK_SETUP.md`
3. 🖼 Sync image storage
4. 🏷 Start annotating

## Help
- Images not showing? → `QUICK_SETUP.md`
- Errors? → `TROUBLESHOOTING.md`

---

**Summary:** You are now on a stable PostgreSQL-backed Label Studio setup with organized documentation and clear workflows. 🎉


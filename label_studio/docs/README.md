# Label Studio for Animal Detector (Documentation Hub)

All Label Studio related documentation has been moved into this `docs/` directory for organization and clarity.

## Current Architecture

The Label Studio setup runs as a Docker Compose stack with three services:
- **label-studio**: Main annotation application (HeartexLabs official image)
- **cloudflared**: Cloudflare Tunnel for secure external access at `https://label.montedelavilla.org`
- **db**: PostgreSQL 15 database for persistent storage

## Quick Start

### Start the Stack
From repository root:
```bash
cd label_studio
docker compose up -d
```

Access Label Studio:
- **Locally**: http://localhost:8080
- **Remote**: https://label.montedelavilla.org (requires Cloudflare Tunnel setup)

### Stop the Stack
```bash
cd label_studio
docker compose down
```

## Documentation Index

### Cloudflare Tunnel Setup
- `CLOUDFLARE_TUNNEL_GUIDE.md` – Full setup and architecture
- `CLOUDFLARE_TUNNEL_SETUP.md` – Alternative step-by-step
- `TUNNEL_QUICK_START.md` – Fast start guide
- `TUNNEL_QUICK_REF.md` – Command cheat sheet
- `SETUP_COMPLETE.md` – Post-setup summary

### Application Usage
- `QUICK_SETUP.md` – Get images showing fast
- `LOGIN_GUIDE.md` – Account creation and login issues
- `CONFIG_GUIDE.md` – Annotation interface configuration
- `FIX_IMAGE_LOADING.md` – Fix broken image loading
- `CSRF_FIX.md` – Resolve CSRF 403 errors behind Cloudflare
- `TROUBLESHOOTING.md` – Common issues and resolutions
- `SOLUTION_SUMMARY.md` – Summary of major fixes applied

## Utilities

The label_studio module provides Python utilities for dataset management:

### Initialize a New Dataset
```bash
python -m label_studio.init_dataset <dataset_name>
```
Creates the directory structure and classes.txt file with default animal classes.

### Convert Label Studio Export to YOLO Format
```bash
python -m label_studio.converter \
  --json data/export/export.json \
  --images datasets/fototrampeo_bosque/images \
  --labels datasets/fototrampeo_bosque/labels \
  --classes datasets/fototrampeo_bosque/labels/classes.txt
```

### Validate YOLO Dataset
```bash
python -m label_studio.validator \
  --images datasets/fototrampeo_bosque/images \
  --labels datasets/fototrampeo_bosque/labels \
  --classes datasets/fototrampeo_bosque/labels/classes.txt
```

## Configuration Files

### Core Files
- `docker-compose.yml` – Service definitions and configuration
- `custom_settings.py` – Django settings override for CSRF and proxy handling
- `label_studio_config.xml` – Annotation interface configuration (animal classes, attributes)
- `config.yml` – Cloudflare Tunnel routing configuration
- `tunnel.env` – Cloudflare credentials (NOT in version control)

### Important Paths
- `data/` – Label Studio database and exports (NOT in version control)
- `../datasets/` – Mounted read-only for image serving
- `/label-studio/data` – Container path for persistent data

## Database

The stack uses PostgreSQL 15 for production-grade persistence:
- Database: `labelstudio`
- User/Password: `postgres/postgres`
- Data stored in Docker volume: `postgres_data`

Previous SQLite database has been migrated to PostgreSQL.

## Security & Access

### CSRF Protection
Custom Django settings configured for Cloudflare Tunnel:
- Trusted origins: `https://label.montedelavilla.org`
- Proxy SSL header handling enabled
- Secure cookies for HTTPS

### File Serving
- Local file serving enabled for dataset images
- Document root: `/datasets` (mapped to `../datasets`)
- SSRF protection disabled to allow local file access

## Cross References
- Main project training docs: `../../docs/` at repository root
- Annotation config: `../label_studio_config.xml`
- Dataset structure: `../../datasets/`

## Maintenance Notes
- Keep environment variables synchronized in `docker-compose.yml` and `custom_settings.py`
- Secure files excluded from git: `tunnel.env`, `config.yml`, `data/`
- Database backup: Export PostgreSQL volume before major changes
- Update `classes.txt` in sync with `label_studio_config.xml` labels

## Last Updated
November 5, 2025


# Label Studio for Animal Detector (Documentation Hub)

All Label Studio related documentation has been moved into this `docs/` directory for organization and clarity.

## Contents

- Cloudflare Tunnel:
  - `CLOUDFLARE_TUNNEL_GUIDE.md` – Full setup and architecture
  - `CLOUDFLARE_TUNNEL_SETUP.md` – Alternative step-by-step
  - `TUNNEL_QUICK_START.md` – Fast start guide
  - `TUNNEL_QUICK_REF.md` – Command cheat sheet
  - `SETUP_COMPLETE.md` – Post-setup summary
- Application Usage:
  - `QUICK_SETUP.md` – Get images showing fast
  - `LOGIN_GUIDE.md` – Account creation and login issues
  - `CONFIG_GUIDE.md` – Annotation interface configuration
  - `FIX_IMAGE_LOADING.md` – Fix broken image loading
  - `CSRF_FIX.md` – Resolve CSRF 403 errors behind Cloudflare
  - `TROUBLESHOOTING.md` – Common issues and resolutions
  - `SOLUTION_SUMMARY.md` – Summary of major fixes applied

## How To Start Label Studio

From repository root:
```bash
cd label_studio
docker compose up -d
firefox http://localhost:8080
```

## Convert / Validate Workflow
```bash
python -m label_studio.converter \
  --json export.json \
  --images datasets/fototrampeo_bosque/images \
  --labels datasets/fototrampeo_bosque/labels \
  --classes datasets/fototrampeo_bosque/labels/classes.txt

python -m label_studio.validator \
  --images datasets/fototrampeo_bosque/images \
  --labels datasets/fototrampeo_bosque/labels \
  --classes datasets/fototrampeo_bosque/labels/classes.txt
```

## Cross References
- Main project training docs: `../docs/` folder at repository root
- Annotation config file: `../label_studio/label_studio_config.xml`

## Maintenance Notes
- Keep environment variable changes mirrored in `docker-compose.yml`
- Secure files: `tunnel.env`, `config.yml`, `data/` stay out of version control

## Last Updated
November 5, 2025


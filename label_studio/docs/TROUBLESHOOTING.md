# Label Studio Troubleshooting Guide

## Problem: Database is Locked Error (FIXED ✅)

**Error Message:**
```
django.db.utils.OperationalError: database is locked
```

**Solution:** Fixed by switching from SQLite to PostgreSQL.

If it reappears:
```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose down
docker compose up -d
```

---

## Problem: Images Won't Load (FIXED ✅)

**Error:**
```
There was an issue loading URL from $image value
```

**Solution:** Corrected hostname + CORS settings in docker-compose.

Restart and clear browser cache:
```bash
docker compose down
docker compose up -d
```

---

## Problem: Can't See Images After Sync

Add local storage correctly:
- **Path:** `/datasets/fototrampeo_bosque/images`
- **Regex:** `.*\.(jpg|jpeg|png|JPG|JPEG|PNG)$`
- ✅ Treat every bucket object as a source file

Sync and refresh.

---

## Problem: Login Issues

Label Studio has **no default credentials**. Create an account on first use.

Forgot password? Change it:
```bash
docker compose exec label-studio python /label-studio/label_studio/manage.py changepassword your-email@localhost
```

---

## Verification Checklist

- [ ] Containers running: `docker compose ps`
- [ ] Access UI: http://localhost:8080
- [ ] Host images exist: `ls datasets/fototrampeo_bosque/images/*.JPG | head`
- [ ] In-container images: `docker exec animal-detector-label-studio ls /datasets/fototrampeo_bosque/images | head`
- [ ] Env vars: `docker exec animal-detector-label-studio env | grep LABEL_STUDIO`
- [ ] Storage configured + synced
- [ ] Tasks visible

---

## Quick Commands
```bash
# Status
docker compose ps

# Logs
docker compose logs --tail=100 | grep -i error

# Restart
docker compose down && docker compose up -d
```

---

## Manual Import (Fallback)
Use UI → Import → Upload Files if local storage path fails.

---

## Need More Help?
- Storage docs: https://labelstud.io/guide/storage.html
- Tunnel docs: See `CLOUDFLARE_TUNNEL_GUIDE.md`


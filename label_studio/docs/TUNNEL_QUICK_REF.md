# Cloudflare Tunnel Quick Reference

## Quick Start
```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose up -d
# Stop
docker compose down
```

## Status
```bash
docker compose ps
cloudflared tunnel info labelstudio-tunnel
```

## Logs
```bash
docker compose logs cloudflared --tail=50
docker compose logs label-studio --tail=50
```

## Access URLs
- Public: https://label.montedelavilla.org
- Local: http://localhost:8080

## Common Actions
```bash
docker compose restart cloudflared
docker compose restart label-studio
curl -I https://label.montedelavilla.org
```

## Diagnostics
```bash
cloudflared tunnel info labelstudio-tunnel
dig label.montedelavilla.org
curl http://localhost:8080
```

## Sensitive Files (Not in Git)
- tunnel.env
- config.yml
- data/

## Tunnel Info
- ID: 3663beb6-957e-4620-99bd-65ac5b9187c1
- Name: labelstudio-tunnel
- Domain: label.montedelavilla.org


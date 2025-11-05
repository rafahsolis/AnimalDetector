# Cloudflare Tunnel Setup for Label Studio

This guide explains how the Cloudflare Zero Trust tunnel is configured to provide secure external access to Label Studio.

## Overview

The setup uses Cloudflare Tunnel to securely expose Label Studio at `https://label.montedelavilla.org` without opening ports on your firewall.

## Architecture

```
Internet → Cloudflare Edge → Cloudflare Tunnel (cloudflared) → Label Studio (Docker)
```

## Configuration Files

### 1. `tunnel.env` (PROTECTED - Not in Git)
Contains sensitive tunnel credentials:
```env
TUNNEL_TOKEN=<your-tunnel-token>
LABEL_STUDIO_HOSTNAME=https://label.montedelavilla.org
```

⚠️ IMPORTANT: This file contains sensitive credentials and is excluded from Git via `.gitignore`.

### 2. `config.yml` (PROTECTED - Not in Git)
Defines tunnel ingress rules:
```yaml
tunnel: 3663beb6-957e-4620-99bd-65ac5b9187c1
credentials-file: /etc/cloudflared/creds.json

ingress:
  - hostname: label.montedelavilla.org
    service: http://label-studio:8080
  - service: http_status:404
```

⚠️ IMPORTANT: The `tunnel` field must use the tunnel ID (UUID), not the tunnel name.

### 3. `tunnel.env.example`
Template for creating your own `tunnel.env` file.

## Setup Instructions

### Prerequisites
- Cloudflare account with domain `montedelavilla.org`
- Docker and Docker Compose installed
- `cloudflared` CLI installed on your system

### Step 1: Authenticate with Cloudflare
```bash
cloudflared tunnel login
```
This creates `~/.cloudflared/cert.pem`.

### Step 2: Create the Tunnel
```bash
cloudflared tunnel create labelstudio-tunnel
```
This creates credentials at `~/.cloudflared/3663beb6-957e-4620-99bd-65ac5b9187c1.json`.

### Step 3: Configure DNS Route
```bash
cloudflared tunnel route dns labelstudio-tunnel label.montedelavilla.org
```
This creates a CNAME record pointing `label.montedelavilla.org` to the tunnel.

### Step 4: Get the Tunnel Token
```bash
cloudflared tunnel token labelstudio-tunnel
```
Copy the token output.

### Step 5: Create Configuration Files
1. Copy `tunnel.env.example` to `tunnel.env`:
   ```bash
   cp tunnel.env.example tunnel.env
   ```
2. Edit `tunnel.env` and paste your tunnel token:
   ```env
   TUNNEL_TOKEN=<paste-token-here>
   LABEL_STUDIO_HOSTNAME=https://label.montedelavilla.org
   ```
3. The `config.yml` file should already exist with the correct configuration.

### Step 6: Start Services
```bash
docker compose up -d
```

### Step 7: Verify
Check that all services are running:
```bash
docker compose ps
docker compose logs cloudflared
```
Verify the tunnel has active connections:
```bash
cloudflared tunnel info labelstudio-tunnel
```
Test external access:
```bash
curl -I https://label.montedelavilla.org
```

## Services
1. **label-studio**: The main Label Studio application
2. **cloudflared**: Cloudflare Tunnel connector
3. **db**: PostgreSQL database for Label Studio

## Troubleshooting

### Tunnel Not Connecting
```bash
docker compose logs cloudflared
cloudflared tunnel info labelstudio-tunnel
docker compose restart cloudflared
```

### Site Not Loading (404)
Ensure `config.yml` uses UUID:
```yaml
tunnel: 3663beb6-957e-4620-99bd-65ac5b9187c1
```
Restart:
```bash
docker compose restart cloudflared
```

### Label Studio Not Accessible
```bash
docker compose logs label-studio
curl http://localhost:8080
docker compose exec label-studio env | grep LABEL_STUDIO_HOSTNAME
```

### CSRF Verification Failed
Add env vars:
```yaml
environment:
  - LABEL_STUDIO_HOST=https://label.montedelavilla.org
  - CSRF_TRUSTED_ORIGINS=https://label.montedelavilla.org
```
Restart and clear cookies.

### DNS Not Resolving
```bash
dig label.montedelavilla.org
cloudflared tunnel route list
```

## Security Notes
- Protect `tunnel.env` and credentials JSON
- Automatic HTTPS via Cloudflare
- No inbound ports exposed

## Protected (Git-ignored) Files
- `tunnel.env`
- `config.yml`
- `data/`

## Monitoring
```bash
cloudflared tunnel info labelstudio-tunnel
docker compose logs -f cloudflared
docker compose logs -f label-studio
```

## Updating
```bash
docker compose pull cloudflared label-studio
docker compose up -d cloudflared label-studio
```

## Backup
```bash
# DB backup
docker compose exec db pg_dump -U postgres labelstudio > labelstudio_backup.sql
# Data dir backup
tar -czf labelstudio_data_backup.tar.gz data/
```

## Restore
```bash
cat labelstudio_backup.sql | docker compose exec -T db psql -U postgres labelstudio
tar -xzf labelstudio_data_backup.tar.gz
```

## Access URLs
- Public: https://label.montedelavilla.org
- Local: http://localhost:8080

## Health Test (Optional)
```python
import unittest, requests
class TestTunnel(unittest.TestCase):
    def test_public_redirect(self):
        r = requests.head("https://label.montedelavilla.org", allow_redirects=False, timeout=10)
        self.assertIn(r.status_code, [200,301,302])
if __name__ == '__main__':
    unittest.main()
```

## References
- Cloudflare Tunnel Docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- Label Studio Docs: https://labelstud.io/guide/

_Last Updated: 2025-11-05_

